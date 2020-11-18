from datetime import datetime

import celery

import celeryconf
from sa import MyDist, MyRow, SESSION_MyRow, SESSION_MyDist

app = celery.Celery(__name__)
app.config_from_object(celeryconf)


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
    from devices import DEMUX

    return celery.chain(
        _demux_run_select.s(DEMUX, cur_ind, duration), _log_demux.s()
    ).apply_async()


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
    from devices import DISTS

    return celery.chain(_dist_run_select.s(DISTS, cur_ind), _log_dist.s()).apply_async()


# dist0 = Entry(
#     "run_dists_0",
#     "cluster.dist_select",
#     schedule=celery.schedules.schedule(run_every=2.1),
#     kwargs={"cur_ind": 0},
#     app=cluster.app,
# )

# demux0 = Entry(
#     "run_demux_0",
#     "cluster.demux_select",
#     schedule=celery.schedules.schedule(run_every=1.3),
#     kwargs={"cur_ind": 0, "duration": 0.3},
#     app=cluster.app,
# )

# demux1 = Entry(
#     "run_demux_1",
#     "cluster.demux_select",
#     schedule=celery.schedules.schedule(run_every=1.3),
#     kwargs={"cur_ind": 1, "duration": 0.3},
#     app=cluster.app,
# )