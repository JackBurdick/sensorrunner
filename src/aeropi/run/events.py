from aeropi.devices.event.device import Event


def build_events_from_config(config):
    events = {}
    try:
        Event_config = config["Event"]
    except KeyError:
        Event_config = None
    if Event_config:
        events["Event"] = Event(Event_config)

    return events