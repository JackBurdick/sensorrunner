import time

import board
import busio

import adafruit_vl53l0x

# https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/python-circuitpython
# scan ic devices
# i2cdetect -y 1
# allow i2c: sudo raspi-config

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
vl53.measurement_timing_budget = 200000  # favor accuracy
# The default timing budget is 33ms

MM_TO_INCH = 0.0393701

for i in range(100):
    try:
        print(f"Range: {vl53.range * MM_TO_INCH: 0.3f} in")
    except OSError:
        pass
    time.sleep(1.0)
