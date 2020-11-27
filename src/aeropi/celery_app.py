import celery
from celery import bootsteps

from celery.bin.base import CeleryOption
import celeryconf

app = celery.Celery("celery_run")

# https://github.com/celery/celery/blob/07000d826573a97ff633b688bda7bf30db114dfe/docs/userguide/extending.rst
# def add_worker_arguments(parser):
#     parser.add_argument("--rawconfig", default=None, help="Config File Required"),


app.user_options["worker"].add(
    CeleryOption("--rawconfig", default=None, help="Config File Required")
)  # add_worker_arguments


class MyBootstep(bootsteps.Step):
    def __init__(self, parent, rawconfig=False, **options):
        super().__init__(parent, **options)
        if rawconfig:
            print(rawconfig)
        else:
            raise ValueError(f"no rawconfig specified")


app.steps["worker"].add(MyBootstep)

# # https://stackoverflow.com/questions/21365101/celery-worker-and-command-line-args
# app.user_options["worker"].add(
#     CeleryOption("--rawconfig", default=None, help="Config File Required")
# )


# class CustomArgs(bootsteps.Step):
#     def __init__(self, worker, rawconfig=None, **options):
#         if rawconfig is not None:
#             print(rawconfig)
#         else:
#             raise ValueError(f"no rawconfig specified")


# app.steps["worker"].add(CustomArgs)

app.config_from_object(celeryconf)
# app.autodiscover_tasks(["tasks.demux.tasks", "tasks.iic.tasks"], force=True)


# aeropi/scratch/config_run/configs/basic_i2c.yml
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0
