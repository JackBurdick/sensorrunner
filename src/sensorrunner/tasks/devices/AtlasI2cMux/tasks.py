# AtlasI2cMux_run
import celery
import importlib

import sensorrunner

importlib.reload(sensorrunner)
from sensorrunner.celery_app import setup_app
from sensorrunner.sa import (
    SESSION_PH_ENTRY,
    PH_ENTRY,
)
from datetime import datetime
from sensorrunner.user_config import USER_CONFIG
from sensorrunner.run.run import build_devices_from_config

AtlasMux = None
app = setup_app()


@app.task(bind=True, queue="q_dists_log")
def _log_dist(self, row):
    if row:
        if isinstance(row, PH_ENTRY):
            row.add(SESSION_PH_ENTRY)
        else:
            raise ValueError(f"unable to match entry {row} to accepted row types")
    else:
        pass


# will use same queue as i2C mux
@app.task(bind=True, queue="q_dists_run")
def _atlas_i2c_run_select(self, dev_dict):
    global AtlasMux
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

    try:
        cur_run_params = dev_dict["params"]["run"]
    except KeyError:
        raise ValueError(
            f"no run params specified for {cur_name}\n> dev_dict: {dev_dict}"
        )

    try:
        unit = cur_run_params["unit"]
    except KeyError:
        raise ValueError(f"no unit is specified for {cur_name}\n> dev_dict: {dev_dict}")

    # NOTE: I'm not sure how best to handle this.. passing through the queue is
    # not currently an options since it is not serialized by standard methods
    if AtlasMux is None:
        iicmux_wrapped = build_devices_from_config(
            {"AtlasI2cMux": USER_CONFIG["AtlasI2cMux"]}
        )
        AtlasMux = iicmux_wrapped["AtlasI2cMux"]
    else:
        pass

    measurement_time = datetime.utcnow()
    cur_v = AtlasMux.return_value(cur_name, cur_run_params)
    post_measurement_time = datetime.utcnow()
    if dev_type == "pH":
        entry = PH_ENTRY(
            name=cur_name, value=cur_v, unit=unit, measurement_time=measurement_time
        )
    else:
        raise ValueError(f"device type {dev_type} unsupported")
    return entry


# @app.task(ignore_result=True)
@app.task(bind=True, queue="collect")
def AtlasI2cMux_run(self, dev_dict):
    return celery.chain(_atlas_i2c_run_select.s(dev_dict), _log_dist.s()).apply_async()
