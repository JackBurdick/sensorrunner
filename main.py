from time import sleep

import typer

from gpiozero import Device, DigitalOutputDevice
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

# GPIO PINS: https://www.raspberrypi.org/documentation/usage/gpio/

"""
TODO:

1. logging
2. organization
3. db hookup
4. config specification

"""


class Demux:
    """
    IMPORTANT: can only be in use one at a time, right now a flag (in_use) is
    used, but maybe this could be controlled outside by a queue in the future?
    (Not sure, because we wouldn't want it to get too large)

    # TODO: convert this to a baseclass
    """

    def __init__(self, ordered_pins, pwr_pin, on_duration=1, stabilize_time=0.05):
        self.pwr = DigitalOutputDevice(pwr_pin)
        self.pwr.off()

        self.select = dict(
            [(i, DigitalOutputDevice(p)) for i, p in enumerate(ordered_pins)]
        )
        self._width = len(self.select)

        if not isinstance(on_duration, (int, float)):
            raise ValueError(
                f"on_duration ({on_duration}) must be type int or float not {type(on_duration)}"
            )
        self.on_duration = on_duration

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
        self.pwr.off()  # TODO: maybe check first?
        bin_rep = self._to_bin(num)
        print(f"on: {bin_rep}")
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].on()
        sleep(self.stabilize_time)  # let stabilize
        self.pwr.on()
        self.in_use = True

    def _off_select(self, num):
        self.pwr.off()  # TODO: maybe check first?
        bin_rep = self._to_bin(num)
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].off()
        self.in_use = False

    def zero(self):
        # first turn power off to prevent accidental other sprays
        self.pwr.off()
        for p in self.select.values():
            p.off()
        self.in_use = False

    def spray_select(self, num, on_duration=None):
        print(f"spray: {num}")  # {vars(self).keys()}
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
        self.pwr.off()
        self.zero()


def main(num: int, dev: bool = False):
    INDEX_PINS = [25, 23, 24, 17]
    PWR_PIN = 27
    # IND_SKIP = [] # TODO: allow for manual off of pins

    typer.echo(f"Run {num}")
    if dev:
        Device.pin_factory = MockFactory()
    else:
        Device.pin_factory = NativeFactory()
    sleep(1)
    sprayer = Demux(INDEX_PINS, PWR_PIN)
    for i in range(16):
        sprayer.spray_select(i)
        sleep(0.5)


if __name__ == "__main__":
    typer.run(main)
