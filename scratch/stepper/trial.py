import sys
import time

from gpiozero import Device, DigitalOutputDevice

# from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()


class Stepper:
    """stepper"""

    def __init__(
        self,
        # init params
        init_config,
        name="stepper",
    ):
        self.name = name
        self.dir_pin = DigitalOutputDevice(init_config["dir"])
        self.step_pin = DigitalOutputDevice(init_config["step"])
        self.pulse_width = 0.0015
        self.time_between = 0.005

    def step(self):
        self.step_pin.on()
        time.sleep(self.pulse_width)
        self.step_pin.off()

    def move_direction(self, num_steps, direction):
        cur_step = 0
        if direction:
            self.dir_pin.on()
        else:
            self.dir_pin.off()

        while cur_step < num_steps:
            self.step()
            print(f"{cur_step}/{num_steps} {direction}")
            cur_step += 1
            time.sleep(self.time_between)


DIRPIN = 27
STEPIN = 17
init_config = {"dir": DIRPIN, "step": STEPIN}
s = Stepper(init_config=init_config)

r_steps = 400
l_steps = 450

s.move_direction(l_steps, True)
time.sleep(0.3)
s.move_direction(r_steps, False)
