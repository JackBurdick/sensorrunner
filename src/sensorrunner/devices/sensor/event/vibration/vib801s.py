from gpiozero import SmoothedInputDevice
import datetime as dt
from sensorrunner.sa import VIB801S_Row
from sensorrunner.tasks.devices.Event.tasks import event_entry


class VIB801S(SmoothedInputDevice):
    """
    vibration
    """

    def __init__(
        self,
        name,
        pin=None,
        pull_up=False,
        active_state=None,
        queue_len=400,
        sample_rate=100,
        threshold=0.5,
        partial=False,
        pin_factory=None,
        when_activated=None,
        when_deactivated=None,
    ):
        super(VIB801S, self).__init__(
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

        if not isinstance(name, str):
            raise ValueError(
                f"name ({name}) expected to be type {str}, not {type(name)}"
            )
        self.name = name

        if when_activated:
            self.when_activated = getattr(self, when_activated)

        if when_deactivated:
            self.when_deactivated = getattr(self, when_deactivated)

    @property
    def value(self):
        return super(VIB801S, self).value

    def add_task(self, state, cur_time):
        # TODO: add task to app
        cur_row = VIB801S_Row(name=self.name, state=state, measurement_time=cur_time)
        event_entry.delay(cur_row)

    def log_when_activated(self):
        cur_time = dt.datetime.utcnow()
        state_name = "on"
        self.add_task(state_name, cur_time)

    def log_when_deactivated(self):
        cur_time = dt.datetime.utcnow()
        state_name = "off"
        self.add_task(state_name, cur_time)
