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

    """

    def __init__(
        self,
        # init params
        name,
        gpio_pins_ordered,
        pwr_pin,
        on_duration=3,
        stabilize_time=0.05,
        # devices
        devices_config=None,
    ):
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

        if not isinstance(on_duration, (int, float)):
            raise ValueError(
                f"on_duration ({on_duration}) must be type int or float not {type(on_duration)}"
            )
        self.on_duration = on_duration

        # name to ind
        self.connected_name_to_ind = self._define_connections(
            gpio_pins_ordered, connected_sensors=devices_config
        )

        self.ind_to_bin = self._num_to_bin(self.connected_name_to_ind.values())

        if not isinstance(stabilize_time, (int, float)):
            raise ValueError(
                f"stabilize_time ({stabilize_time}) must be type int or float not {type(stabilize_time)}"
            )
        self.stabilize_time = stabilize_time

        self.in_use = False  # attempt at preventing multiple calls at the same time

        self.zero()

    def _to_bin(self, num: int):
        if not isinstance(num, int):
            raise ValueError(f"{num} is not int")
        return f"{num:b}".zfill(self._width)

    def _num_to_bin(self, connected_inds):
        ind_to_bin = {}
        for ind in connected_inds:
            ind_to_bin[ind] = self._to_bin(ind)
        return ind_to_bin

    def _define_connections(self, index_pins, connected_sensors):
        avail_connects = range(len(index_pins) ** 2)
        connected = {}
        for name, sensor_d in connected_sensors:
            cur_ind = sensor_d["index"]
            if cur_ind not in avail_connects:
                raise ValueError(f"cur_ind not available in {avail_connects}")
            else:
                connected[name] = cur_ind
        return connected

    def _on_select(self, index):
        if self.in_use:
            raise ValueError(f"can only be in use once at a time, currently in use!")
        self.zero()
        try:
            bin_rep = self.ind_to_bin[index]
        except KeyError:
            raise KeyError(
                f"index {index} is not available in {self.ind_to_bin.keys()}"
            )
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].on()
        sleep(self.stabilize_time)  # let stabilize
        self.pwr.on()
        self.in_use = True

    def _off_select(self, index):
        self.pwr.off()  # TODO: maybe check first?
        bin_rep = self.ind_to_bin[index]
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

    def _run_select(self, num, on_duration=None):
        if on_duration:
            if not isinstance(on_duration, (int, float)):
                raise ValueError(
                    f"on_duration ({on_duration}) must be type int or float not {type(on_duration)}"
                )
            duration = on_duration
        else:
            duration = self.on_duration
        start = dt.datetime.utcnow()
        self._on_select(num)
        sleep(duration)
        self.zero()
        stop = dt.datetime.utcnow()
        return (start, stop)

    def return_value(self, name, on_duration=None):
        try:
            num = self.connected_name_to_ind[name]
        except KeyError:
            raise KeyError(
                f"device {self.name} does not have device named {name}\n"
                f"please select from {self.connected_name_to_ind.keys()}"
            )
        out = self._run_select(num, on_duration)
        return out
