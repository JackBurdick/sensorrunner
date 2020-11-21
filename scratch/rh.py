import time

import typer

import adafruit_si7021
import adafruit_tca9548a
import board
import busio

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# mux
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x72)


# each sensor
rht_sensor = adafruit_si7021.SI7021(tca2[2])


def main(num: int = 100):
    for i in range(num):
        try:
            a_t = rht_sensor.temperature * 1.8 + 32
        except OSError:
            a_t = None
        try:
            a_rh = rht_sensor.relative_humidity
        except OSError:
            a_rh = None

        print(f"env. {a_t: 0.3f}*f {a_rh: 0.3f}%")
        time.sleep(1.0)


if __name__ == "__main__":
    typer.run(main)
