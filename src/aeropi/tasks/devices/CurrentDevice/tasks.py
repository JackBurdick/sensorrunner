import importlib
from datetime import datetime

import celery

import aeropi
from aeropi.celery_app import app
from aeropi.user_config import USER_CONFIG
from aeropi.run.run import build_devices_from_config
from aeropi.sa import CurrentDevice, SESSION_CurrentDevice

importlib.reload(aeropi)

CURRENTDEVICE_Dev = None


@app.task(bind=True, queue="q_device")
def _log_device(self, row):
    if row:
        if isinstance(row, CurrentDevice):
            row.add(SESSION_CurrentDevice)
        else:
            raise ValueError(f"unable to match entry {row} to accepted row types")
    else:
        pass


@app.task(bind=True, queue="q_device")
def _run_device(self, dev_dict):
    global CURRENTDEVICE_Dev
    # https://docs.celeryproject.org/en/latest/userguide/tasks.html#instantiation
    if dev_dict is None:
        raise ValueError("no dev_dict is present")

    try:
        cur_name = dev_dict["name"]
    except KeyError:
        raise ValueError(f"no name is specified in {dev_dict}\n> dev_dict: {dev_dict}")

    try:
        dev_type = dev_dict["device_type"]
    except KeyError:
        raise ValueError(
            f"no `device_type` specified for {cur_name}\n> dev_dict: {dev_dict}"
        )

    # NOTE: I'm not sure how best to handle this.. passing through the queue is
    # not currently an options since it is not serialized by standard methods
    if CURRENTDEVICE_Dev is None:
        device_wrapped = build_devices_from_config(
            {"CurrentDevice": USER_CONFIG["CurrentDevice"]}
        )
        CURRENTDEVICE_Dev = device_wrapped["CurrentDevice"]
    else:
        pass

    measurement_time = datetime.utcnow()
    cur_stats = CURRENTDEVICE_Dev.return_value()
    if dev_type == "current_device":
        entry = CurrentDevice(
            name=cur_name, measurement_time=measurement_time, **cur_stats
        )
    else:
        raise ValueError(f"device type {dev_type} unsupported")
    return entry


# @app.task(ignore_result=True)
@app.task(bind=True, queue="collect")
def CurrentDevice_run(self, dev_dict):
    return celery.chain(_run_device.s(dev_dict), _log_device.s()).apply_async()
