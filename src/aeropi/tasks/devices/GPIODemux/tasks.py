import celery
from aeropi.celery_app import app
from aeropi.sa import MyRow, SESSION_MyRow
import datetime as dt
import time
from aeropi.celery_app import USER_CONFIG
from aeropi.run.run import build_devices_from_config

GPIODEMUX = None


@app.task(bind=True, queue="q_demux_log")
def _log_demux(self, row):
    if row:
        if isinstance(row, MyRow):
            # global SESSION_MyRow
            row.add(SESSION_MyRow)
        else:
            raise ValueError(f"unable to match entry {row} to accepted row types")
    else:
        pass


@app.task(bind=True, queue="q_demux_run")
def _demux_run_select(self, dev_dict, wait_secs=0.1):
    global GPIODEMUX
    # https://docs.celeryproject.org/en/latest/userguide/tasks.html#instantiation
    if dev_dict is None:
        raise ValueError("no dev_dict is present")

    try:
        cur_name = dev_dict["name"]
    except KeyError:
        raise ValueError(f"no name is specified in {dev_dict}")

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
    if GPIODEMUX is None:
        gpio_demux_wrapped = build_devices_from_config(
            {"GPIODemux": USER_CONFIG["GPIODemux"]}
        )
        GPIODEMUX = gpio_demux_wrapped["GPIODemux"]
    else:
        pass

    wait = dt.timedelta(seconds=wait_secs).seconds

    # run device
    # TODO: will need to alter this in the future depending on the device type
    start, stop = GPIODEMUX.return_value(cur_name, cur_run_params)

    # allow wait between devices
    time.sleep(max(0, wait))

    if dev_type == "switch_low":
        #  db entry
        entry = MyRow(index=cur_name, start=start, stop=stop, unit=unit)
    else:
        entry = None

    return entry


@app.task(bind=True, queue="collect")
def GPIODemux_run(self, dev_dict):
    return celery.chain(_demux_run_select.s(dev_dict), _log_demux.s()).apply_async()
