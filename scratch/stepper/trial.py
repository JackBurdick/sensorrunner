import sys
import RPi.GPIO as gpio 
import time


gpio.setmode(gpio.BCM)

r_steps = 400
l_steps = 450


DIRPIN = 27
STEPIN = 17
gpio.setwarnings(False)
gpio.setup(DIRPIN, gpio.OUT)
gpio.setup(STEPIN, gpio.OUT)

L_DIR = True
R_DIR = False

time.sleep(0.5)


def move_direction(num_steps, direction):
    time_between = 0.005
    pulse_time = 0.0015
    cur_step = 0
    gpio.output(DIRPIN, direction)
    while cur_step < num_steps:
        gpio.output(STEPIN, True)
        time.sleep(pulse_time)
        gpio.output(STEPIN, False)
        print(f"{num_steps} {direction}")
        cur_step += 1
        time.sleep(time_between)


move_direction(l_steps, L_DIR)
time.sleep(0.3)
move_direction(r_steps, R_DIR)

gpio.cleanup()
