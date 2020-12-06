import signal

from aeropi.devices.event.device import Event
from aeropi.user_config import USER_CONFIG


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
    # obtain parse config
    events = build_events_from_config(USER_CONFIG)

    print(events)

    try:
        signal.pause()
    except KeyboardInterrupt:
        print("ending events")
