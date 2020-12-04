from gpiozero import SmoothedInputDevice
import datetime as dt


class VIB801S(SmoothedInputDevice):
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
            raise

        self.when_activated = self.log_when_activated
        self.when_deactivated = self.log_when_deactivated

    @property
    def value(self):
        return super(VIB801S, self).value

    def add_task(self, state, cur_time):
        # TODO: add task to app
        print(f"{state}: {cur_time}")

    def log_when_activated(self):
        cur_time = dt.datetime.utcnow()
        state_name = "on"
        self.add_task(state_name, cur_time)

    def log_when_deactivated(self):
        cur_time = dt.datetime.utcnow()
        state_name = "off"
        self.add_task(state_name, cur_time)
