import crummycm as ccm
import signal

from aeropi.config.template import TEMPLATE
from aeropi.devices.event.device import Event
from aeropi.secrets import L_CONFIG_DIR, P_CONFIG_DIR


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
    try:
        out = ccm.generate(L_CONFIG_DIR, TEMPLATE)
    except FileNotFoundError:
        out = ccm.generate(P_CONFIG_DIR, TEMPLATE)
    events = build_events_from_config(out)

    print(events)

    try:
        signal.pause()
    except KeyboardInterrupt:
        print("ending events")
