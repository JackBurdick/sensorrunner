import time

import typer

from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory
from gpiozero import DigitalOutputDevice, LineSensor, DistanceSensor


# GPIO PINS: https://www.raspberrypi.org/documentation/usage/gpio/

"""
TODO:

"""


def main(rounds: int = 100, dev: bool = False):
    ECHO = 14
    TRGR = 15

    if dev:
        Device.pin_factory = MockFactory()
    else:
        Device.pin_factory = NativeFactory()

    # 14.5in = 0.3683m
    dist = DistanceSensor(ECHO, TRGR, max_distance=0.3683)
    while True:
        print(f"distance: {dist.distance}")
        time.sleep(1)


if __name__ == "__main__":
    typer.run(main)
