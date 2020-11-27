import celery
import celeryconf
import crummycm as ccm
from kombu import Queue
from aeropi.config.template import TEMPLATE
from pathlib import Path

app = celery.Celery("celery_run")


# obtain parse config
out = ccm.generate(
    "/home/pi/dev/aeropi/scratch/config_run/configs/basic_i2c.yml", TEMPLATE
)
print("=====" * 8)
print(out)
print("=====" * 8)


# set Queues
tmp = list(celeryconf.task_queues)
tmp.extend(
    [
        Queue("q_demux_run"),
        Queue("q_demux_log"),
        Queue("q_dists_run"),
        Queue("q_dists_log"),
    ]
)
celeryconf.task_queues = tuple(tmp)


app.config_from_object(celeryconf)

DEV_TASK_DIR = "./tasks"


def obtain_relevant_task_dirs(out):
    # NOTE: I'm not sure how I want to link the name to tasks. Right now I like
    # the concept of having a separate tasks directory, but that may change such
    # that the tasks are in the devices location and only highlevel/catchall
    # tasks are in the tasks directory
    dirs = []
    device_tasks = [
        x.name for x in list(filter(lambda x: x.is_dir(), Path(DEV_TASK_DIR).iterdir()))
    ]
    for dev_name in out.keys():
        if dev_name in device_tasks:
            dirs.append(dev_name)
    return dirs


dirs = obtain_relevant_task_dirs(out)
print(dirs)
dir_name = DEV_TASK_DIR.split("/")[-1]
d_names = []
for d in dirs:
    d_names.append(f"{dir_name}.{d}")
print(d_names)
app.autodiscover_tasks(d_names, force=True)
# app.autodiscover_tasks(["tasks.demux.tasks", "tasks.iic.tasks"], force=True)


# aeropi/scratch/config_run/configs/basic_i2c.yml
# possibly helpful later:
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0
