from aeropi.devices.sensor.event.vibration.vib801s import VIB801S


class Event:
    def __init__(self, devices_dict):

        self.ALLOWED_DEVICES = {"vib801s": VIB801S}
        self.ALLOWED_EVENTS = ["when_activated", "when_deactivated"]

        if devices_dict is None:
            raise ValueError("no devices specified in `device_dict`")

        devices = {}
        for name, dd in devices_dict.items():
            devices[name] = {}
            if dd["device_type"] not in self.ALLOWED_DEVICES:
                raise ValueError(
                    f"device_type {dd['device_type']} of {name} is not allowed"
                    f"\nPlease select from {self.ALLOWED_DEVICES.keys()}"
                )
            cur_dev_class = self.ALLOWED_DEVICES[dd["device_type"]]
            try:
                params = dd["params"]
            except KeyError:
                params = None

            # set event functions
            devices[name]["events"] = {}
            available_fns = [
                f
                for f in dir(cur_dev_class)
                if callable(getattr(cur_dev_class, f)) and not f.startswith("_")
            ]
            for event_name in self.ALLOWED_EVENTS:
                try:
                    fn_name = params["events"][event_name]
                except KeyError:
                    fn_name = None
                if fn_name is not None:
                    if fn_name not in available_fns:
                        raise ValueError(
                            f"specified fn ({fn_name}) for {name} not available for {cur_dev_class}.\n"
                            f"please select from {available_fns}"
                        )
                    devices[name]["events"][event_name] = fn_name
            # initialize device with user params
            if params:
                init_params = params["init"]
            else:
                init_params = {}
            cur_params = {**init_params, **devices[name]["events"]}
            cur_device = cur_dev_class(name, **cur_params)
            devices[name]["device"] = cur_device

        self.devices = devices