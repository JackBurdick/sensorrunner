import celery
import importlib

importlib.reload(aeropi)
from aeropi.celery_app import app
from aeropi.sa import VL53l0X, SI7021, SESSION_VL53l0X, SESSION_SI7021
from datetime import datetime
from aeropi.celery_app import USER_CONFIG
from aeropi.run.run import build_devices_from_config

IICMUX = None


@app.task(bind=True, queue="q_dists_log")
def _log_dist(self, row):
    if row:
        if isinstance(row, VL53l0X):
            row.add(SESSION_VL53l0X)
        elif isinstance(row, SI7021):
            row.add(SESSION_SI7021)
        else:
            raise ValueError(f"unable to match entry {row} to accepted row types")
    else:
        pass


@app.task(bind=True, queue="q_dists_run")
def _i2c_run_select(self, dev_dict):
    global IICMUX
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
    if IICMUX is None:
        iicmux_wrapped = build_devices_from_config({"I2CMux": USER_CONFIG["I2CMux"]})
        IICMUX = iicmux_wrapped["I2CMux"]
    else:
        pass

    measurement_time = datetime.utcnow()
    cur_v = IICMUX.return_value(cur_name, cur_run_params)
    if dev_type == "vl53l0x":
        entry = VL53l0X(
            name=cur_name, value=cur_v, unit=unit, measurement_time=measurement_time
        )
    elif dev_type == "si7021":
        entry = SI7021(
            name=cur_name,
            temp_value=cur_v[0],
            temp_unit=unit,
            rh_value=cur_v[1],
            rh_unit="%",
            measurement_time=measurement_time,
        )
    else:
        raise ValueError(f"device type {dev_type} unsupported")
    return entry


# @app.task(ignore_result=True)
@app.task(bind=True, queue="collect")
def I2CMux_run(self, dev_dict):
    return celery.chain(_i2c_run_select.s(dev_dict), _log_dist.s()).apply_async()
