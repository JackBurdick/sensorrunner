import celery
import celeryconf


app = celery.Celery("celery_run")

app.config_from_object(celeryconf)
# app.autodiscover_tasks(["tasks.demux.tasks", "tasks.iic.tasks"], force=True)


# aeropi/scratch/config_run/configs/basic_i2c.yml
# possibly helpful later:
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0
