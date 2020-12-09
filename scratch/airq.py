import time

import typer

from adafruit_pm25.i2c import PM25_I2C
import adafruit_tca9548a
import board
import busio

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# mux
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x72)


# each sensor
aq_sensor = PM25_I2C(tca2[2])


def main(num: int = 100):
    for i in range(num):
        try:
            aqdata = aq_sensor.read()
        except RuntimeError:
            aqdata = None

        print(
            f"standard: {aqdata['pm10 standard']}, {aqdata['pm25 standard']}, {aqdata['pm100 standard']}"
        )
        print(f"Env: {aqdata['pm10 env']}, {aqdata['pm25 env']}, {aqdata['pm100 env']}")
        print(f"Particles > 0.3um / 0.1L air: {aqdata['particles 03um']}")
        print(f"Particles > 0.5um / 0.1L air: {aqdata['particles 05um']}")
        print(f"Particles > 1.0um / 0.1L air: {aqdata['particles 10um']}")
        print(f"Particles > 2.5um / 0.1L air: {aqdata['particles 25um']}")
        print(f"Particles > 5.0um / 0.1L air: {aqdata['particles 50um']}")
        print(f"Particles > 10 um / 0.1L air: {aqdata['particles 100um']}")
        time.sleep(1.0)


if __name__ == "__main__":
    typer.run(main)
