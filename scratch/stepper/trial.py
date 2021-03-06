import sys
import time

from gpiozero import Device, DigitalOutputDevice, SmoothedInputDevice

# from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()

import datetime as dt


class Hall(SmoothedInputDevice):
    """
    vibration
    """

    def __init__(
        self,
        name,
        pin=None,
        pull_up=True,
        active_state=None,
        queue_len=5,
        # sample_rate=100,
        # threshold=0.5,
        partial=False,
        pin_factory=None,
        when_activated=None,
        when_deactivated=None,
    ):
        super().__init__(
            pin,
            pull_up=pull_up,
            active_state=active_state,
            # threshold=threshold,
            # queue_len=queue_len,
            # sample_wait=1 / sample_rate,
            partial=partial,
            pin_factory=pin_factory,
        )
        try:
            self._queue.start()
        except:
            self.close()
            raise

        if not isinstance(name, str):
            raise ValueError(
                f"name ({name}) expected to be type {str}, not {type(name)}"
            )
        self.name = name

        # if when_activated:
        #     self.when_activated = getattr(self, when_activated)

        # if when_deactivated:
        #     self.when_deactivated = getattr(self, when_deactivated)

    @property
    def value(self):
        return super(Hall, self).value


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
        self.loc_pin = Hall(name="location", pin=init_config["location"])
        self.pulse_width = 0.0015
        self.time_between = 0.005

        # TODO: logic to set zero/record positions
        # TODO: logic to roughly caclulate distances/locations

    def step(self):
        self.step_pin.on()
        time.sleep(self.pulse_width)
        self.step_pin.off()

    def at_location(self):
        return self.loc_pin.value

    def move_direction(self, num_steps, direction):
        cur_step = 0
        if direction:
            self.dir_pin.on()
        else:
            self.dir_pin.off()

        while cur_step < num_steps:
            if self.at_location():
                print(f"stop - location: {cur_step}")
                break
            else:
                self.step()
                print(f"{cur_step}/{num_steps} {direction}")
                cur_step += 1
                time.sleep(self.time_between)


DIRPIN = 27
STEPIN = 17
LOCPIN = 23
init_config = {"dir": DIRPIN, "step": STEPIN, "location": LOCPIN}
s = Stepper(init_config=init_config)


r_steps = 500
l_steps = 550

s.move_direction(l_steps, True)
time.sleep(0.3)
s.move_direction(r_steps, False)
