import celery
from .device import DEMUX
from aeropi.celery_app import app
from aeropi.sa import MyRow, SESSION_MyRow
from datetime import datetime


@app.task(bind=True, queue="q_demux_log")
def _log_demux(self, row):
    global SESSION_MyRow
    row.add(SESSION_MyRow)


@app.task(bind=True, queue="q_demux_run")
def _demux_run_select(self, cur_ind, duration):
    global DEMUX
    global MyRow
    start = datetime.utcnow()
    DEMUX.run_select(cur_ind, on_duration=duration)
    stop = datetime.utcnow()
    entry = MyRow(index=cur_ind, start=start, stop=stop)
    return entry


@app.task(bind=True, queue="collect")
def demux_select(self, cur_ind, duration):
    return celery.chain(
        _demux_run_select.s(cur_ind, duration), _log_demux.s()
    ).apply_async()
