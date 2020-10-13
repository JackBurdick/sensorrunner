import time

import typer

from demux import Demux
from gpiozero import Device
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


def loop_sprayer(sprayer):
    for i in sprayer.connect_inds:
        sprayer.run_select(i)
        time.sleep(0.5)  # rest between each


def main(hours: int = None, dev: bool = False):
    INDEX_PINS = [25, 23, 24, 17]
    PWR_PIN = 27
    UNCONNECTED = [11, 12, 13, 14, 15]  # TODO: allow for manual off of pins
    CONNECTED = []
    DELAY_MIN = 3
    ON_DURATION = 3

    if dev:
        Device.pin_factory = MockFactory()
    else:
        Device.pin_factory = NativeFactory()

    sprayer = Demux(
        INDEX_PINS,
        PWR_PIN,
        connected=CONNECTED,
        unconnected=UNCONNECTED,
        on_duration=ON_DURATION,
    )
    time.sleep(2)

    try:
        if hours:
            time_start = time.monotonic()
            time_end = time_start + (60 * (60 * hours))
            while time.monotonic() < time_end:
                print(
                    f"duration: {time.monotonic()-time_start:.1f} < {time_end-time_start:.1f} min"
                )
                loop_sprayer(sprayer)
                time.sleep((60 * DELAY_MIN))
        else:
            count = 0
            time_start = time.monotonic()
            while True:
                count += 1
                print(f"loop: {count} min: {(time.monotonic()-time_start):.1f}")
                loop_sprayer(sprayer)
                time.sleep((60 * DELAY_MIN))
    except KeyboardInterrupt:
        sprayer.zero()
        print("sprayer zeroed")


if __name__ == "__main__":
    typer.run(main)
