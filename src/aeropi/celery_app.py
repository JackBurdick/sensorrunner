import celery
import celeryconf


app = celery.Celery("celery_run")
app.config_from_object(celeryconf)
app.autodiscover_tasks(["tasks.demux.tasks", "tasks.iic.tasks"], force=True)
