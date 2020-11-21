import time

import typer

import adafruit_tca9548a
import adafruit_vl53l0x
import board
import busio

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# mux
tca = adafruit_tca9548a.TCA9548A(i2c, address=0x70)
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x72)


# each sensor
vl53_a = adafruit_vl53l0x.VL53L0X(tca[0])
vl53_a.measurement_timing_budget = 200000

vl53_b = adafruit_vl53l0x.VL53L0X(tca[1])
vl53_b.measurement_timing_budget = 200000
# The default timing budget is 33ms


vl53_c = adafruit_vl53l0x.VL53L0X(tca2[0])
vl53_d = adafruit_vl53l0x.VL53L0X(tca2[1])

MM_TO_INCH = 0.0393701


def main(num: int = 100):
    for i in range(num):
        try:
            a_in = f"{vl53_a.range * MM_TO_INCH: 0.3f}"
        except OSError:
            a_in = None
        try:
            b_in = f"{vl53_b.range * MM_TO_INCH: 0.3f}"
        except OSError:
            b_in = None
        try:
            c_in = f"{vl53_c.range * MM_TO_INCH: 0.3f}"
        except OSError:
            c_in = None
        try:
            d_in = f"{vl53_d.range * MM_TO_INCH: 0.3f}"
        except OSError:
            d_in = None
        print(f"dist. a:{a_in} b: {b_in}, c:{c_in}, d:{d_in}")
        time.sleep(1.0)


if __name__ == "__main__":
    typer.run(main)
