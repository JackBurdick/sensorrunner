import datetime as dt
from time import sleep

from gpiozero import Device, DigitalOutputDevice

# from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()


class GPIODemux:
    """
    IMPORTANT: can only be in use one at a time, right now a flag (in_use) is
    used, but maybe this could be controlled outside by a queue in the future?
    (Not sure, because we wouldn't want it to get too large) - note this logic
    likely belongs in the config

    TODO: mirror I2C device specification of sensors

    """

    def __init__(
        self,
        # init params
        name,
        init_config,
        # devices
        devices_config,
    ):
        STABILIZE_TIME = 0.05
        if not isinstance(STABILIZE_TIME, (int, float)):
            raise ValueError(
                f"stabilize_time ({STABILIZE_TIME}) must be type int or float not {type(STABILIZE_TIME)}"
            )
        self.stabilize_time = STABILIZE_TIME

        gpio_pins_ordered = init_config["gpio_pins_ordered"]
        pwr_pin = init_config["pwr_pin"]

        if not isinstance(name, str):
            raise ValueError(
                f"name ({name}) expected to be type {str}, not {type(name)}"
            )
        self.name = name

        if not isinstance(pwr_pin, int):
            raise ValueError(
                f"pwr_pin ({pwr_pin}) expected to be type {int}, not {type(pwr_pin)}"
            )
        self.pwr = DigitalOutputDevice(pwr_pin)
        self.pwr.off()

        self.select = dict(
            [(i, DigitalOutputDevice(p)) for i, p in enumerate(gpio_pins_ordered)]
        )
        self._width = len(self.select)

        # name to ind
        self.connected_name_to_conf = self._define_connections(
            gpio_pins_ordered, connected_sensors=devices_config
        )

        self.in_use = False  # attempt at preventing multiple calls at the same time

        self.zero()

    def _to_bin(self, num: int):
        if not isinstance(num, int):
            raise ValueError(f"{num} is not int")
        return f"{num:b}".zfill(self._width)

    def _define_connections(self, index_pins, connected_sensors):
        # self.ind_to_bin = self._num_to_bin(self.connected_name_to_conf.values())
        avail_connects = range(len(index_pins) ** 2)
        connected = {}
        for name, sensor_d in connected_sensors.items():
            connected[name] = {}
            # index
            cur_ind = sensor_d["index"]
            if cur_ind not in avail_connects:
                raise ValueError(f"cur_ind not available in {avail_connects}")
            connected[name]["index"] = cur_ind
            connected[name]["bin"] = self._to_bin(cur_ind)
        return connected

    def _on_select(self, bin_rep):
        if self.in_use:
            raise ValueError(f"can only be in use once at a time, currently in use!")
        self.zero()
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].on()
        sleep(self.stabilize_time)  # let stabilize
        self.pwr.on()
        self.in_use = True

    def _off_select(self, bin_rep):
        self.pwr.off()  # TODO: maybe check first?
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].off()
        self.in_use = False

    def zero(self):
        # first turn power off to prevent accidental other runs
        self.pwr.off()
        sleep(self.stabilize_time)
        for p in self.select.values():
            p.off()
        self.in_use = False

    def _run_select(self, dev_dict, on_duration):
        # num = dev_dict["index"]
        bin_rep = dev_dict["bin"]
        on_duration = dev_dict["on_duration"]
        if on_duration:
            if not isinstance(on_duration, (int, float)):
                raise ValueError(
                    f"on_duration ({on_duration}) must be type {int} or {float} not {type(on_duration)}"
                )
            duration = on_duration
        else:
            raise ValueError(
                f"No on_duration specified for {dev_dict} in device {self.name}"
            )

        start = dt.datetime.utcnow()
        self._on_select(bin_rep)
        sleep(duration)
        self.zero()
        stop = dt.datetime.utcnow()
        return (start, stop)

    def return_value(self, name, params):
        try:
            dev_dict = self.connected_name_to_conf[name]
        except KeyError:
            raise KeyError(
                f"device {self.name} does not have device named {name}\n"
                f"please select from {self.connected_name_to_conf.keys()}"
            )

        # TODO: clunky
        if params:
            try:
                on_duration = params["on_duration"]
            except KeyError:
                raise ValueError(f"must specify the on_duration for {name}")
        else:
            raise ValueError(f"no run params specified for {name}")

        out = self._run_select(dev_dict, on_duration)
        return out

    @staticmethod
    def build_task_params(device_name, device_dict):
        """
        demux0 = Entry(
            "run_demux_0",
            "tasks.demux.tasks.demux_select",
            schedule=celery.schedules.schedule(run_every=1.8),
            kwargs={"cur_ind": 0, "duration": 0.35},
            app=app,
        )

        {
            "a": {
                "index": 0,
                "device_type": "switch_low",
                "params": {
                    "run": {"on_duration": 1.7, "unit": "seconds"},
                    "schedule": {"frequency": 4.0},
                },
                "fn_name": None,
            },
            "b": {
                "index": 1,
                "device_type": "switch_low",
                "params": {
                    "run": {"on_duration": 1.3, "unit": "seconds"},
                    "schedule": {"frequency": 3.0},
                },
                "fn_name": None,
            },
        }

        """
        DEFAULT_FN_NAME = "return_value"
        entry_specs = {}
        for comp_name, comp_dict in device_dict.items():
            entry_d = {}
            fn_name = comp_dict["fn_name"]
            if fn_name is None:
                fn_name = DEFAULT_FN_NAME
            entry_d["name"] = f"{device_name}_{comp_name}_{fn_name}"
            # TODO: make more robust
            entry_d["task"] = "aeropi.tasks.devices.GPIODemux.tasks.GPIODemux_run"
            # maybe make schedule outside this?
            entry_d["run_every"] = comp_dict["params"]["schedule"]["frequency"]
            cur_kwargs = comp_dict["params"]["run"]
            if not isinstance(cur_kwargs, dict):
                raise ValueError(
                    f"run params ({cur_kwargs}) expected to be type {dict}, not {type(cur_kwargs)}"
                )
            entry_d["kwargs"] = {"dev_dict": cur_kwargs}
            entry_specs[comp_name] = entry_d
        return entry_specs

