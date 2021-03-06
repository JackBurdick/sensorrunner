from gpiozero import SmoothedInputDevice
import datetime as dt
imoprt time


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
        #queue_len=100,
        #sample_rate=100,
        #threshold=0.5,
        partial=False,
        pin_factory=None,
        when_activated=None,
        when_deactivated=None,
    ):
        super(Hall, self).__init__(
            pin,
            pull_up=pull_up,
            active_state=active_state,
            threshold=threshold,
            #queue_len=queue_len,
            #sample_wait=1 / sample_rate,
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

        # if when_activated:
        #     self.when_activated = getattr(self, when_activated)

        # if when_deactivated:
        #     self.when_deactivated = getattr(self, when_deactivated)

    @property
    def value(self):
        return super(Hall, self).value

    # def log_when_activated(self):
    #     cur_time = dt.datetime.utcnow()
    #     print(f"ACTIVE: {cur_time} - {self.value()}")

    # def log_when_deactivated(self):
    #     cur_time = dt.datetime.utcnow()
    #     print(f"ACTIVE: {cur_time} - {self.value()}")


h = Hall(name="hall", pin=23)

for i in range(30):
    print(i, h.value())
    time.sleep(0.3)
