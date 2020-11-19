import celery
import celeryconf


app = celery.Celery(__name__)
app.config_from_object(celeryconf)
app.autodiscover_tasks(
    ["celery_run.tasks.demux.tasks", "celery_run.tasks.i2c.tasks"], force=True
)
