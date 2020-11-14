

## Cheatsheet

```bash
conda env export | grep -v "^prefix: " > aerodev.yml
```

```bash
conda env create -f aerodev.yml
```

```bash
pip install typer
pip install -U black
pip install gpiozero pigpio

```



## tof

https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/python-circuitpython

```bash
pip install adafruit-circuitpython-vl53l0x
pip install adafruit-circuitpython-tca9548a
```

### GPIO
# https://www.raspberrypi.org/documentation/usage/gpio/
```bash
pinout
```

### scan all ic devices

scan ic devices
```bash
# allow i2c: sudo raspi-config
i2cdetect -y 1
```