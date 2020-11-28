import adafruit_tca9548a
import board
import busio
from aeropi.devices.sensor.I2C.air.si7021 import SI7021
from aeropi.devices.sensor.I2C.distance.vl53l0x import VL5310X

import celery

# from aeropi.celery_app import app
# from redbeat import RedBeatSchedulerEntry as Entry


class I2CMux:
    def __init__(self, devices_dict, SCL_pin=board.SCL, SDA_pin=board.SDA):
        # NOTE: accepting tuples currently because I'm not sure what the config
        # will look like yet

        # "fn": None --> resort to default fn
        self.ALLOWED_DEVICES = {
            "vl53l0x": {"device_class": VL5310X, "fn": None},
            "si7021": {"device_class": SI7021, "fn": None},
        }

        # connected = (name, address, channel, device, fn)
        if devices_dict is None:
            raise ValueError("no devices specified in `device_dict`")

        # Initialize I2C bus and sensor.
        i2c = busio.I2C(SCL_pin, SDA_pin)

        #     addr_to_tca[addr] = adafruit_tca9548a.TCA9548A(i2c, address=addr)
        # TODO: ensure no channel duplicates
        addr_to_tca = {}
        devices = {}
        for name, dd in devices_dict.items():
            devices[name] = {}
            cur_dev_class = self.ALLOWED_DEVICES[dd["device_type"]]["device_class"]
            if dd["address"] not in addr_to_tca:
                addr_to_tca[dd["address"]] = adafruit_tca9548a.TCA9548A(
                    i2c, address=dd["address"]
                )
            cur_tca = addr_to_tca[dd["address"]]
            cur_device = cur_dev_class(cur_tca[dd["channel"]])
            devices[name]["device_type"] = cur_device
            available_fns = [
                f
                for f in dir(cur_device)
                if callable(getattr(cur_device, f)) and not f.startswith("_")
            ]
            try:
                dev_fn = dd["fn_name"]
            except KeyError:
                dev_fn = None
            if dev_fn is not None:
                if dev_fn not in available_fns:
                    raise ValueError(
                        f"specified fn ({dev_fn}) for {name} not available for {cur_device}.\n"
                        f"please select from {available_fns}"
                    )
                fn_name = dev_fn
            else:
                fn_name = "return_value"
            try:
                devices[name]["fn"] = getattr(devices[name]["device_type"], fn_name)
            except KeyError:
                raise ValueError(
                    f"specified fn ({fn_name}) for {name} not available for {cur_device}.\n"
                    f"please select from {available_fns}"
                )
        self.devices = devices

    def return_value(self, name, **kwargs):
        if name is None:
            return ValueError(
                f"no name specified. please select from {self.devices.keys()}"
            )
        if not isinstance(name, str):
            return ValueError(f"`name` is expected to be type {str}, not {type(name)}")
        try:
            dev_d = self.devices[name]
        except KeyError:
            raise ValueError(
                f"{name} is not available. please select from {self.devices.keys()}"
            )
        value = dev_d["fn"](**kwargs)
        return value

    @staticmethod
    def build_task_params(device_name, device_dict):
        """
        dist0 = Entry(
            "run_dist_0",
            "tasks.iic.tasks.dist_select",
            schedule=celery.schedules.schedule(run_every=2),
            kwargs={"cur_ind": 0},
            app=celery_app.app,
        )
        # name=None, task=None, schedule=None, kwargs, app

        {
            "env_a": {
                "channel": 2,
                "address": 114,
                "device_type": "si7021",
                "params": {"run": {"unit": "f"}, "schedule": {"frequency": 1800.0}},
                "fn_name": None,
            },
            "dist_a": {
                "channel": 0,
                "address": 112,
                "device_type": "vl53l0x",
                "params": {"run": {"unit": "in"}, "schedule": {"frequency": 1800.0}},
                "fn_name": None,
            },
        }
        """
        DEFAULT_FN_NAME = "return_value"

        entry_specs = {}
        for comp_name, comp_dict in device_dict.items():
            entry_d = {}
            fn_name = comp_dict["fn_name"]
            if fn_name is None:
                fn_name = DEFAULT_FN_NAME
            entry_d["name"] = f"{device_name}_{comp_name}_{fn_name}"
            # TODO: make more robust
            entry_d["task"] = "tasks.devices.I2CMux.tasks.I2CMux_run"
            # maybe make schedule outside this?
            entry_d["run_every"] = comp_dict["params"]["schedule"]["frequency"]
            cur_kwargs = comp_dict["params"]["run"]
            if not isinstance(cur_kwargs, dict):
                raise ValueError(
                    f"run params ({cur_kwargs}) expected to be type {dict}, not {type(cur_kwargs)}"
                )
            entry_d["kwargs"] = cur_kwargs
            entry_specs[comp_name] = entry_d
        return entry_specs
