import time

import board
import busio

import adafruit_vl53l0x

# https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/python-circuitpython

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
vl53.measurement_timing_budget = 200000  # favor accuracy
# The default timing budget is 33ms


for i in range(100):
    print(f"Range: {vl53.range}mm")
    time.sleep(1.0)