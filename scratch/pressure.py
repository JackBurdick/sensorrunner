import time

import typer

import adafruit_bmp3xx
import adafruit_tca9548a
import board
import busio

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# mux
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x72)


# each sensor
press_sensor = adafruit_bmp3xx.BMP3XX_I2C(tca2[2])
press_sensor.pressure_oversampling = 8
press_sensor.temperature_oversampling = 2


def main(num: int = 100):
    for i in range(num):
        try:
            a_t = press_sensor.temperature * 1.8 + 32
        except OSError:
            a_t = None
        try:
            a_pr = press_sensor.pressure
        except OSError:
            a_pr = None

        print(f"env. {a_t: 0.3f}*f pressure: {a_pr: 0.3f} Pa")
        time.sleep(1.0)


if __name__ == "__main__":
    typer.run(main)
