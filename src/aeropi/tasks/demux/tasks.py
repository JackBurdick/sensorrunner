import celery
from .device import DEMUX
#from ...celery_app import app
from celery_run.celery_app import app
from ..sa import MyRow, SESSION_MyRow
import datetime


@app.task(bind=True, queue="q_demux_log")
def _log_demux(self, row):
    global SESSION_MyRow
    row.add(SESSION_MyRow)


@app.task(bind=True, queue="q_demux_run")
def _demux_run_select(self, demux, cur_ind, duration):
    start = datetime.utcnow()
    demux.run_select(cur_ind, on_duration=duration)
    stop = datetime.utcnow()
    entry = MyRow(index=cur_ind, start=start, stop=stop)
    return entry


@app.task(bind=True, queue="collect")
def demux_select(self, cur_ind, duration):
    global DEMUX

    return celery.chain(
        _demux_run_select.s(DEMUX, cur_ind, duration), _log_demux.s()
    ).apply_async()
