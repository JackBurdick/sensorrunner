from time import sleep

import time
import typer

from gpiozero import Device, DigitalOutputDevice
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

# GPIO PINS: https://www.raspberrypi.org/documentation/usage/gpio/

"""
TODO:

0. config specification
1. logging
2. organization
3. db hookup

"""


class Demux:
    """
    IMPORTANT: can only be in use one at a time, right now a flag (in_use) is
    used, but maybe this could be controlled outside by a queue in the future?
    (Not sure, because we wouldn't want it to get too large)

    # TODO: convert this to a baseclass
    """

    def __init__(
        self,
        gpio_pins_ordered,
        pwr_pin,
        on_duration=3,
        stabilize_time=0.05,
        connected=None,
        unconnected=None,
    ):
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

        self.connect_inds = self._define_connections(
            gpio_pins_ordered, connected=connected, unconnected=unconnected
        )
        self.num_to_bin = self._num_to_bin(self.connect_inds)

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

    def _on_select(self, num):
        if self.in_use:
            raise ValueError(f"can only be in use once at a time, currently in use!")
        self.zero()
        try:
            bin_rep = self.num_to_bin[num]
        except KeyError:
            raise KeyError(f"num {num} is not available in {self.num_to_bin.keys()}")
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].on()
        sleep(self.stabilize_time)  # let stabilize
        self.pwr.on()
        self.in_use = True

    def _off_select(self, num):
        self.pwr.off()  # TODO: maybe check first?
        bin_rep = self.num_to_bin[num]
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

    def _num_to_bin(self, nums):
        num_bin = {}
        for v in nums:
            num_bin[v] = self._to_bin(v)
        return num_bin

    def _define_connections(self, index_pins, connected=None, unconnected=None):
        avail_connects = len(index_pins) ** 2
        if connected and unconnected:
            raise ValueError(
                f"please only specify connected ({connected}) or unconnected ({unconnected}), not both"
            )
        elif connected:
            CONNECT_INDS = connected
        elif unconnected:
            CONNECT_INDS = [i for i in range(avail_connects) if i not in unconnected]
        else:
            CONNECT_INDS = [i for i in range(avail_connects)]
        return CONNECT_INDS

    def run_select(self, num, on_duration=None):
        print(f"on: {num}", end=" ")  # {vars(self).keys()}
        if on_duration:
            if not isinstance(on_duration, (int, float)):
                raise ValueError(
                    f"on_duration ({on_duration}) must be type int or float not {type(on_duration)}"
                )
            duration = on_duration
        else:
            duration = self.on_duration
        self._on_select(num)
        sleep(duration)
        self.zero()
        print(" --> off")


def main(num: int, dev: bool = False):
    INDEX_PINS = [25, 23, 24, 17]
    PWR_PIN = 27
    UNCONNECTED = []  # TODO: allow for manual off of pins
    CONNECTED = [1]

    if dev:
        Device.pin_factory = MockFactory()
    else:
        Device.pin_factory = NativeFactory()

    sprayer = Demux(INDEX_PINS, PWR_PIN, connected=CONNECTED, unconnected=UNCONNECTED)
    sleep(2)
    time_start = time.monotonic()
    time_end = time_start + 60 * num
    DELAY_MIN = 3
    try:
        while time.monotonic() < time_end:
            now = time.monotonic()
            print(f"duration: {now:.1f} < {time_end:.1f}")
            for i in sprayer.connect_inds:
                sprayer.run_select(i)
                sleep(0.5)  # rest between each
            sleep((60 * DELAY_MIN))
    except KeyboardInterrupt:
        sprayer.zero()
        print("sprayer zeroed")


if __name__ == "__main__":
    typer.run(main)
