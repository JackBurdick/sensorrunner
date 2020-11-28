import celery
from redbeat import RedBeatSchedulerEntry as Entry

import crummycm as ccm
from aeropi.celery_app import app
from aeropi.config.template import TEMPLATE
from aeropi.run.run import build_devices_from_config, build_task_params_from_config
from aeropi.secrets import L_CONFIG_DIR, P_CONFIG_DIR

try:
    out = ccm.generate(L_CONFIG_DIR, TEMPLATE)
except FileNotFoundError:
    out = ccm.generate(P_CONFIG_DIR, TEMPLATE)
USER_CONFIG = out

# print("start")
conf = ccm.generate(USER_CONFIG, TEMPLATE)
devs = build_devices_from_config(conf)
task_params = build_task_params_from_config(conf)

entries = {}
for device_type, device_task_spec in task_params.items():
    for dev_name, dev_spec in device_task_spec.items():
        for comp_name, comp_task_spec in dev_spec.items():
            name = comp_task_spec["name"]
            entry = Entry(
                name,
                comp_task_spec["task"],
                schedule=celery.schedules.schedule(
                    run_every=comp_task_spec["run_every"]
                ),
                kwargs=comp_task_spec["kwargs"],
                app=app,
            )
            entries[name] = entry
print(entries)
