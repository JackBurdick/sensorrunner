import celery
from celery import bootsteps
from celery.bin import Option
import celeryconf


app = celery.Celery("celery_run")

# # https://stackoverflow.com/questions/21365101/celery-worker-and-command-line-args
app.user_options["worker"].add(
    Option(
        "--config_file", dest="raw_config", default=None, help="Config File Required"
    )
)


class CustomArgs(bootsteps.Step):
    def __init__(self, worker, raw_config=None, **options):
        if raw_config is not None:
            print(raw_config)
        else:
            raise ValueError(f"no config_file specified")


app.steps["worker"].add(CustomArgs)

app.config_from_object(celeryconf)
# app.autodiscover_tasks(["tasks.demux.tasks", "tasks.iic.tasks"], force=True)


# aeropi/scratch/config_run/configs/basic_i2c.yml
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0

