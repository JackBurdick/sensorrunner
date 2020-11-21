import celery
from .device import DEMUX
from aeropi.celery_app import app
from aeropi.sa import MyRow, SESSION_MyRow
import datetime as dt
import time


@app.task(bind=True, queue="q_demux_log")
def _log_demux(self, row):
    global SESSION_MyRow
    row.add(SESSION_MyRow)


@app.task(bind=True, queue="q_demux_run")
def _demux_run_select(self, cur_ind, duration, wait_secs=0.1):
    global DEMUX
    global MyRow
    wait = dt.timedelta(seconds=wait_secs).seconds
    # TODO: push timekeeping to the device
    start = dt.datetime.utcnow()
    DEMUX.run_select(cur_ind, on_duration=duration)
    stop = dt.datetime.utcnow()

    # allow wait between devices
    time.sleep(max(0, wait))
    entry = MyRow(index=cur_ind, start=start, stop=stop)
    return entry


@app.task(bind=True, queue="collect")
def demux_select(self, cur_ind, duration):
    return celery.chain(
        _demux_run_select.s(cur_ind, duration), _log_demux.s()
    ).apply_async()
