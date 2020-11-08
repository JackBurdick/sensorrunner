import time

import typer

from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory
from gpiozero import DigitalOutputDevice, SmoothedInputDevice

# GPIO PINS: https://www.raspberrypi.org/documentation/usage/gpio/

"""
TODO:

0. config specification
1. logging
2. organization
3. db hookup

"""


class Dist:
    """"""

    def __init__(
        self,
        trigger_pin,
        echo_pin,
    ):

        self.trigger = DigitalOutputDevice(trigger_pin)
        self.trigger.off()

        self.echo = SmoothedInputDevice(pin=echo_pin)

    def get_dist(self):
        # trigger
        self.trigger.on()
        time.sleep(0.00001)
        self.trigger.off()

        start_time = None
        count = 0
        while not self.echo.is_active():
            start_time = time.time()
            count += 1
            if count > 1000:
                start_time = None
                break

        print(f"start time {start_time}")

        end_time = None
        count = 0
        while not self.echo.is_active():
            end_time = time.time()
            count += 1
            if count > 1000:
                start_time = None
                break
        print(f"end time {end_time}")

        distance = (end_time - start_time) * 17150
        return distance

    def zero(self):
        self.trigger.off()


def main(rounds: int = 100, dev: bool = False):
    TRGR = 15
    ECHO = 1

    if dev:
        Device.pin_factory = MockFactory()
    else:
        Device.pin_factory = NativeFactory()

    my_dist = Dist(trigger_pin=TRGR, echo_pin=ECHO)
    time.sleep(0.5)

    try:
        for i in range(rounds):
            distance = my_dist.get_dist()
            print(f"cur_dist: {distance}")
            time.sleep(1)
    except KeyboardInterrupt:
        my_dist.zero()
        print(f"{my_dist.__class__.__name__} zeroed")
    finally:
        my_dist.zero()


if __name__ == "__main__":
    typer.run(main)
