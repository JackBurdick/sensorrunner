from aeropi.devices.sensor.spi.adc.light.pt19 import PT19
from gpiozero import MCP3008, Device

# from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()


class MDC3800:
    def __init__(
        self,
        name,
        init_config,
        # devices
        devices_dict,
    ):
        # NOTE: accepting tuples currently because I'm not sure what the config
        # will look like yet

        # "fn": None --> resort to default fn
        self.ALLOWED_DEVICES = {"pt19": {"device_class": PT19, "fn": None}}

        # connected = (name, address, channel, device, fn)
        if devices_dict is None:
            raise ValueError("no devices specified in `device_dict`")

        # TODO: assure pins are valid/acceptable

        # light = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9,
        # select_pin=8)
        # TODO: ensure channel 0-8

        channel_to_device = {}
        devices = {}
        for name, dd in devices_dict.items():
            devices[name] = {}
            cur_dev_class = self.ALLOWED_DEVICES[dd["device_type"]]["device_class"]
            if dd["channel"] not in channel_to_device:
                channel_to_device[dd["channel"]] = MCP3008(
                    channel=dd["channel"],
                    clock_pin=11,
                    mosi_pin=10,
                    miso_pin=9,
                    select_pin=8,
                )
            cur_device = channel_to_device[dd["channel"]]
            cur_device_obj = cur_dev_class(cur_device)

            # TODO: this really isn't a device_type but a device_object - same
            # in I2C
            devices[name]["device_type"] = cur_device_obj
            available_fns = [
                f
                for f in dir(cur_device)
                if callable(getattr(cur_device, f)) and not f.startswith("_")
            ]
            try:
                dev_fn = dd["fn_name"]
            except KeyError:
                dev_fn = None
            if dev_fn is not None:
                if dev_fn not in available_fns:
                    raise ValueError(
                        f"specified fn ({dev_fn}) for {name} not available for {cur_device}.\n"
                        f"please select from {available_fns}"
                    )
                fn_name = dev_fn
            else:
                fn_name = "return_value"
            try:
                devices[name]["fn"] = getattr(devices[name]["device_type"], fn_name)
            except KeyError:
                raise ValueError(
                    f"specified fn ({fn_name}) for {name} not available for {cur_device}.\n"
                    f"please select from {available_fns}"
                )
        self.devices = devices

    def return_value(self, name, params):
        if name is None:
            return ValueError(
                f"no name specified. please select from {self.devices.keys()}"
            )
        if not isinstance(name, str):
            return ValueError(f"`name` is expected to be type {str}, not {type(name)}")
        try:
            dev_d = self.devices[name]
        except KeyError:
            raise ValueError(
                f"{name} is not available. please select from {self.devices.keys()}"
            )
        if params:
            value = dev_d["fn"](**params)
        else:
            # TODO: try
            value = dev_d["fn"]()
        return value

    @staticmethod
    def build_task_params(device_name, device_dict):
        """
        dist0 = Entry(
            "run_dist_0",
            "tasks.iic.tasks.dist_select",
            schedule=celery.schedules.schedule(run_every=2),
            kwargs={},
            app=celery_app.app,
        )
        # name=None, task=None, schedule=None, kwargs, app

        {
            "env_a": {
                "channel": 2,
                "address": 114,
                "device_type": "si7021",
                "params": {"run": {"unit": "f"}, "schedule": {"frequency": 1800.0}},
                "fn_name": None,
            },
            "dist_a": {
                "channel": 0,
                "address": 112,
                "device_type": "vl53l0x",
                "params": {"run": {"unit": "in"}, "schedule": {"frequency": 1800.0}},
                "fn_name": None,
            },
        }
        """
        DEFAULT_FN_NAME = "return_value"

        entry_specs = {}
        for comp_name, comp_dict in device_dict.items():
            dev_dict = comp_dict.copy()
            entry_d = {}
            fn_name = comp_dict["fn_name"]
            if fn_name is None:
                fn_name = DEFAULT_FN_NAME
            entry_d["name"] = f"{device_name}_{comp_name}_{fn_name}"
            # TODO: make more robust
            entry_d["task"] = "aeropi.tasks.devices.MDC3800.tasks.MDC3800_run"
            # maybe make schedule outside this?
            entry_d["run_every"] = comp_dict["params"]["schedule"]["frequency"]
            if not isinstance(dev_dict, dict):
                raise ValueError(
                    f"run params ({dev_dict}) expected to be type {dict}, not {type(dev_dict)}"
                )
            # add component name
            dev_dict["name"] = comp_name
            entry_d["kwargs"] = {"dev_dict": dev_dict}
            entry_specs[comp_name] = entry_d
        return entry_specs
