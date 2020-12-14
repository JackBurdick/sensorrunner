import signal

from sensorrunner.devices.event.device import Event
from sensorrunner.user_config import USER_CONFIG


def build_events_from_config(config):
    events = {}
    try:
        Event_config = config["Event"]
    except KeyError:
        Event_config = None
    if Event_config:
        events["Event"] = Event(Event_config)

    return events


if __name__ == "__main__":
    events = build_events_from_config(USER_CONFIG)
    try:
        signal.pause()
    except KeyboardInterrupt:
        print("ending events")
