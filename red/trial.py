import time

import typer

from demux import Demux
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

import board
import busio
import adafruit_tca9548a
import adafruit_vl53l0x


MM_TO_INCH = 0.0393701


def loop_sprayer(sprayer):
    for i in sprayer.connect_inds:
        sprayer.run_select(i)
        time.sleep(0.5)  # rest between each


def main(dev: bool = False):
    INDEX_PINS = [25, 23, 24, 17]
    PWR_PIN = 27
    UNCONNECTED = [11, 12, 13, 14, 15]  # TODO: allow for manual off of pins
    CONNECTED = []
    DELAY_SEC = 3
    ON_DURATION = 1

    LOOPS = 10

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

    # TODO: use only single pin lib
    # Initialize I2C bus and sensor.
    i2c = busio.I2C(board.SCL, board.SDA)

    # mux
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # each sensor
    vl53_a = adafruit_vl53l0x.VL53L0X(tca[0])
    vl53_a.measurement_timing_budget = 200000

    vl53_b = adafruit_vl53l0x.VL53L0X(tca[1])
    vl53_b.measurement_timing_budget = 200000
    # The default timing budget is 33ms

    # init
    time.sleep(2)
    try:
        for i in range(LOOPS):
            # sprayer
            loop_sprayer(sprayer)
            print("done sprayer")

            # dist
            try:
                a_in = f"{vl53_a.range * MM_TO_INCH: 0.3f}"
            except OSError:
                a_in = None
            try:
                b_in = f"{vl53_b.range * MM_TO_INCH: 0.3f}"
            except OSError:
                b_in = None
            print(f"dist. a:{a_in} b: {b_in}")

            time.sleep(DELAY_SEC)

    except KeyboardInterrupt:
        sprayer.zero()
        print("sprayer zeroed")


if __name__ == "__main__":
    typer.run(main)