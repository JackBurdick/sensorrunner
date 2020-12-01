import time

import typer

import adafruit_tca9548a
import adafruit_veml6070
import board
import busio

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# mux
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x72)


# each sensor
uv_sensor = adafruit_veml6070.VEML6070(tca2[4])


def main(num: int = 100):
    for i in range(num):
        try:
            uv = uv_sensor.uv_raw
        except OSError:
            uv = None

        print(f"uv. {uv: 0.3f}")
        time.sleep(1.0)


if __name__ == "__main__":
    typer.run(main)
