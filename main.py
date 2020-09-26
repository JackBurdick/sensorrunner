import typer
from gpiozero.pins.mock import MockFactory

from gpiozero import Device, DigitalOutputDevice
from time import sleep

# GPIO PINS: https://www.raspberrypi.org/documentation/usage/gpio/


class Solenoid:
    def __init__(self, pin_num):
        self.pin_num = pin_num
        self.out = DigitalOutputDevice(pin_num)

    def spray(self):
        print(f"spray {self.pin_num}")
        self.out.on()
        sleep(1)
        self.out.off()


class Solenoids:
    def __init__(self):
        self.S0 = Solenoid(23)
        self.S1 = Solenoid(24)
        self.S2 = Solenoid(17)
        self.S3 = Solenoid(27)

    def spray(self):

        print(f"spray: {vars(self).keys()}")
        for name, s in vars(self).items():
            s.spray()


def main(num: int, dev: bool = False):
    typer.echo(f"Run {num}")
    if dev:
        Device.pin_factory = MockFactory()
    sleep(1)
    solenoids = Solenoids()
    solenoids.spray()


if __name__ == "__main__":
    typer.run(main)