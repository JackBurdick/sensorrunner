import celery
from .device import DISTS
from aeropi.celery_app import app
from aeropi.sa import MyDist, SESSION_MyDist
import datetime


@app.task(bind=True, queue="q_dists_log")
def _log_dist(self, row):
    global SESSION_MyDist
    row.add(SESSION_MyDist)


@app.task(bind=True, queue="q_dists_run")
def _dist_run_select(self, dists, cur_ind):
    UNIT = "in"
    PRECISION = 4
    measurement_time = datetime.utcnow()
    cur_v = dists.obtain_reading(cur_ind, precision=PRECISION, unit=UNIT)
    entry = MyDist(
        index=cur_ind, value=cur_v, unit=UNIT, measurement_time=measurement_time
    )
    return entry


@app.task(bind=True, queue="collect")
def dist_select(self, cur_ind):
    global DISTS

    return celery.chain(_dist_run_select.s(DISTS, cur_ind), _log_dist.s()).apply_async()
