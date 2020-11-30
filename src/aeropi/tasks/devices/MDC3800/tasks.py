import importlib
from datetime import datetime

import celery

import aeropi
from aeropi.celery_app import USER_CONFIG, app
from aeropi.run.run import build_devices_from_config
from aeropi.sa import PT19, SESSION_PT19

importlib.reload(aeropi)

MDC3800_Dev = None


@app.task(bind=True, queue="q_mdc3800_log")
def _log_mdc3800(self, row):
    if row:
        if isinstance(row, PT19):
            row.add(SESSION_PT19)
        else:
            raise ValueError(f"unable to match entry {row} to accepted row types")
    else:
        pass


@app.task(bind=True, queue="q_mdc3800_return_value")
def _mdc3800_run_select(self, dev_dict):
    global MDC3800_Dev
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
    if MDC3800_Dev is None:
        mdc3800_wrapped = build_devices_from_config({"I2CMux": USER_CONFIG["MDC3800"]})
        MDC3800_Dev = mdc3800_wrapped["MDC3800"]
    else:
        pass

    measurement_time = datetime.utcnow()
    cur_v = MDC3800_Dev.return_value(cur_name, cur_run_params)
    if dev_type == "pt19":
        entry = PT19(
            name=cur_name, value=cur_v, unit=unit, measurement_time=measurement_time
        )
    else:
        raise ValueError(f"device type {dev_type} unsupported")
    return entry


# @app.task(ignore_result=True)
@app.task(bind=True, queue="collect")
def MDC3800_run(self, dev_dict):
    return celery.chain(_mdc3800_run_select.s(dev_dict), _log_mdc3800.s()).apply_async()
