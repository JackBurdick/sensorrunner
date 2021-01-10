import celery
import importlib
import requests
import urllib3

import sensorrunner

importlib.reload(sensorrunner)
from sensorrunner.celery_app import setup_app
from sensorrunner.sa import ESPCAM_Row, SESSION_ESPCAM
from datetime import datetime
from sensorrunner.user_config import USER_CONFIG
from sensorrunner.run.run import build_devices_from_config

CAMSDICT = None
app = setup_app()


@app.task(bind=True, queue="q_cam_log")
def _log_cam(self, row):
    if row:
        if isinstance(row, ESPCAM_Row):
            row.add(SESSION_ESPCAM)
        else:
            raise ValueError(f"unable to match entry {row} to accepted row types")
    else:
        pass


def _return_entry(dev_dict):
    global CAMSDICT
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

    # NOTE: I'm not sure how best to handle this.. passing through the queue is
    # not currently an options since it is not serialized by standard methods
    if CAMSDICT is None:
        CAMSDICT_wrapped = build_devices_from_config({"Cams": USER_CONFIG["Cams"]})
        CAMSDICT = CAMSDICT_wrapped["Cams"]
    else:
        pass

    """
    name = Column(String)
    bucket = Column(String)
    index = Column(String)
    capture_time = Column(TIMESTAMP)
    post_capture_time = Column(TIMESTAMP)
    file_path = Column(String)
    ip = Column(String)
    """

    ret_dict = CAMSDICT.return_value(cur_name, cur_run_params)
    post_capture_time = datetime.utcnow()
    # CAMDICT
    if dev_type == "ESPCam":
        entry = ESPCAM_Row(
            name=cur_name,
            bucket=cur_run_params["bucket"],
            index=cur_run_params["index"],
            capture_time=ret_dict["capture_time"],
            post_capture_time=post_capture_time,
            file_path=ret_dict["file_path"],
            ip=CAMSDICT.devices[cur_name]["device_type"].ip_addr,
        )

    else:
        raise ValueError(f"device type {dev_type} unsupported")
    return entry


@app.task(bind=True, queue="q_cam_run", max_retries=5, soft_time_limit=30)
def _cams_run_select(self, dev_dict):

    try:
        entry = _return_entry(dev_dict)
    except Exception as e:
        # TODO: log error
        num_retries = self.request.retries
        seconds_to_wait = 2.0 ** num_retries
        try:
            raise self.retry(exc=e, countdown=seconds_to_wait)
        except (
            celery.exceptions.MaxRetriesExceededError,
            urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.NewConnectionError,
            requests.exceptions.ConnectionError,
            OSError,
        ) as e:
            # TODO log e
            entry = None

    return entry


# @app.task(ignore_result=True)
@app.task(bind=True, queue="collect")
def Cams_run(self, dev_dict):
    return celery.chain(_cams_run_select.s(dev_dict), _log_cam.s()).apply_async()
