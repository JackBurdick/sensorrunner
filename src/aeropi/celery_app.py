import celery
from celery import bootsteps
from celery.bin.base import CeleryOption
import celeryconf


app = celery.Celery("celery_run")

# # https://stackoverflow.com/questions/21365101/celery-worker-and-command-line-args
app.user_options["worker"].add(
    CeleryOption("--config_file", default=None, help="Config File Required")
)


class CustomArgs(bootsteps.Step):
    def __init__(self, worker, config_file=None, **options):
        if config_file is not None:
            print(config_file)
        else:
            raise ValueError(f"no config_file specified")


app.steps["worker"].add(CustomArgs)

app.config_from_object(celeryconf)
# app.autodiscover_tasks(["tasks.demux.tasks", "tasks.iic.tasks"], force=True)


# aeropi/scratch/config_run/configs/basic_i2c.yml
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0

