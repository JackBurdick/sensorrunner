import signal

from gpiozero import Device, SmoothedInputDevice
from gpiozero.pins.native import NativeFactory

Device.pin_factory = NativeFactory()


class VibrationSensor(SmoothedInputDevice):
    """
    vibration
    """

    def __init__(
        self,
        pin=None,
        pull_up=False,
        active_state=None,
        queue_len=400,
        sample_rate=100,
        threshold=0.5,
        partial=False,
        pin_factory=None,
    ):
        super(VibrationSensor, self).__init__(
            pin,
            pull_up=pull_up,
            active_state=active_state,
            threshold=threshold,
            queue_len=queue_len,
            sample_wait=1 / sample_rate,
            partial=partial,
            pin_factory=pin_factory,
        )
        try:
            self._queue.start()
        except:
            self.close()
            raise

        self.when_activated = self.on
        self.when_deactivated = self.off

    @property
    def value(self):
        return super(VibrationSensor, self).value

    def on(self):
        print("on")

    def off(self):
        print("off")


vib_sensor = VibrationSensor(22)


if __name__ == "__main__":
    signal.pause()
