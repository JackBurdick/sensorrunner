import celery
import celeryconf
import crummycm as ccm
from aeropi.config.template import TEMPLATE

app = celery.Celery("celery_run")

print(celeryconf)

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
