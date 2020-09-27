from time import sleep

import typer

from gpiozero import Device, DigitalOutputDevice
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

# GPIO PINS: https://www.raspberrypi.org/documentation/usage/gpio/


class Demux:
    def __init__(self, ordered_pins, pwr_pin):
        self.select = dict(
            [(i, DigitalOutputDevice(p)) for i, p in enumerate(ordered_pins)]
        )
        self.pwr = DigitalOutputDevice(pwr_pin)
        self._width = len(self.select)

        self.zero()
        self.pwr.off()

    def _to_bin(self, num: int):
        if not isinstance(num, int):
            raise ValueError(f"{num} is not int")
        return f"{num:b}".zfill(self._width)

    def on_select(self, num):
        self.zero()
        self.pwr.off()  # TODO: maybe check first?
        bin_rep = self._to_bin(num)
        print(f"on: {bin_rep}")
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].on()
                sleep(0.1)  # let stabilize
        self.pwr.on()

    def off_select(self, num):
        self.pwr.off()  # TODO: maybe check first?
        bin_rep = self._to_bin(num)
        for i, v in enumerate(bin_rep[::-1]):
            if int(v):
                self.select[i].off()

    def zero(self):
        for p in self.select.values():
            p.off()
        self.pwr.off()

    def spray_select(self, num):
        print(f"spray: {num}")  # {vars(self).keys()}
        self.on_select(num)
        sleep(1)
        # self.off_select(num)
        self.zero()


def main(num: int, dev: bool = False):
    typer.echo(f"Run {num}")
    if dev:
        Device.pin_factory = MockFactory()
    else:
        Device.pin_factory = NativeFactory()
    sleep(1)
    dm = Demux([23, 24, 17], 27)
    for i in range(8):
        sleep(0.5)
        dm.spray_select(i)


if __name__ == "__main__":
    typer.run(main)
