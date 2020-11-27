import celery
import celeryconf
import crummycm as ccm
from kombu import Queue
from aeropi.config.template import TEMPLATE

app = celery.Celery("celery_run")


# Queue("q_demux_run"),
# Queue("q_demux_log"),
# Queue("q_dists_run"),
# Queue("q_dists_log"),
print(celeryconf.task_queues)
tmp = list(celeryconf.task_queues)
tmp.extend(
    [
        Queue("q_demux_run"),
        Queue("q_demux_log"),
        Queue("q_dists_run"),
        Queue("q_dists_log"),
    ]
)
tmp = tuple(tmp)
print(tmp)
celeryconf.task_queues = tmp
print(celeryconf.task_queues)

app.config_from_object(celeryconf)

out = ccm.generate(
    "/home/pi/dev/aeropi/scratch/config_run/configs/basic_i2c.yml", TEMPLATE
)
print("=====" * 8)
print(out)
print("=====" * 8)

# app.autodiscover_tasks(["tasks.demux.tasks", "tasks.iic.tasks"], force=True)


# aeropi/scratch/config_run/configs/basic_i2c.yml
# possibly helpful later:
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0
