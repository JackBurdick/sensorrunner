# from datetime import datetime

# import celery

# import celeryconf
# from sa import MyDist, MyRow, SESSION_MyRow, SESSION_MyDist

# app = celery.Celery(__name__)
# app.config_from_object(celeryconf)


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