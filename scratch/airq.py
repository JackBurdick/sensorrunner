import time

import typer
from collections import Counter

from adafruit_pm25.i2c import PM25_I2C
import adafruit_tca9548a
import board
import busio

from gpiozero import Device, DigitalOutputDevice
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)

# mux
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x72)

pwr_pin = DigitalOutputDevice(6)

# each sensor
pwr_pin.on()
time.sleep(1)
aq_sensor = PM25_I2C(tca2[2])
# pwr_pin.off() ignore for this example


# spec:
# https://cdn-shop.adafruit.com/product-files/4632/4505_PMSA003I_series_data_manual_English_V2.6.pdf
# other information:
# https://forums.adafruit.com/viewtopic.php?f=48&t=136528#p676664

# sampling rate 2.3 seconds


def average_dict(v_dicts):
    # filter values with None
    for k_d, v_d in v_dicts.items():
        if v_d:
            v_dicts[k_d] = {k: v for k, v in v_d.items() if v is not None}

    # calculate average
    occurance, sums = Counter(), Counter()
    for n, sensor_ret_d in v_dicts.items():
        sums.update(sensor_ret_d)
        occurance.update(sensor_ret_d.keys())

    avg_res = {x: float(sums[x]) / occurance[x] for x in sums.keys()}
    return avg_res


def parse_sensor(aq_sensor):
    try:
        aqdata = aq_sensor.read()
    except OSError:
        print("ERROR!")
        aqdata = None

    vals, units = {}, {}
    if aqdata:
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

        for skt in sensor_keys:
            vals[skt[2]] = aqdata[skt[0]]
            units[skt[2]] = skt[1]
    return vals, units


def main(num: int = 100):
    for i in range(num):
        NUM_ITERATIONS = 3

        # turn on
        pwr_pin.on()
        print("initializing...")
        time.sleep(45)
        print("ready")

        raw_vals = {}
        for i in range(NUM_ITERATIONS):
            cur_v, cur_u = parse_sensor(aq_sensor)
            print("----------" * 8)
            print("IT: {i}")
            print(cur_v)
            time.sleep(10)
            raw_vals[f"{i}"] = cur_v

        print("----------" * 8)
        avg_vals = average_dict(raw_vals)
        print(avg_vals)

        pwr_pin.off()
        time.sleep(15)
        print("sleeping")


if __name__ == "__main__":
    typer.run(main)
