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


# spec:
# https://cdn-shop.adafruit.com/product-files/4632/4505_PMSA003I_series_data_manual_English_V2.6.pdf
# other information:
# https://forums.adafruit.com/viewtopic.php?f=48&t=136528#p676664

# sampling rate 2.3 seconds


def main(num: int = 100):
    for i in range(num):
        try:
            aqdata = aq_sensor.read()
        except RuntimeError:
            aqdata = None

        # keys
        # reading key, unit, new_name
        # Particle Matter concentrations of different size particles in micro-gram per cubic meter
        sensor_keys = [
            ("particles 03um", "03um/0.1L", "03um"),
            ("particles 05um", "05um/0.1L", "05um"),
            ("particles 10um", "10um/0.1L", "10um"),
            ("particles 25um", "25um/0.1L", "25um"),
            ("particles 50um", "50um/0.1L", "50um"),
            ("particles 100um", "100um/0.1L", "100um"),
            ("pm10 standard", "ug/m^3", "standard_pm10"),
            ("pm10 env", "ug/m^3", "pm10"),
            ("pm25 standard", "ug/m^3", "standard_pm25"),
            ("pm25 env", "ug/m^3", "pm25"),
            ("pm100 standard", "ug/m^3", "standard_pm100"),
            ("pm100 env", "ug/m^3", "pm100"),
        ]

        vals = {}
        for skt in sensor_keys:
            vals[skt[2]] = (aqdata[skt[0]], skt[1])

        print(vals)

        time.sleep(1.0)


if __name__ == "__main__":
    typer.run(main)
