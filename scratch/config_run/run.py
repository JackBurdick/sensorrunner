import celery
from redbeat import RedBeatSchedulerEntry as Entry

import time
import crummycm as ccm
from aeropi.celery_app import setup_app
from aeropi.config.template import TEMPLATE
from aeropi.run.run import build_devices_from_config, build_task_params_from_config
from aeropi.secrets import L_CONFIG_DIR, P_CONFIG_DIR


def create_task_entries(task_params):
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
                    app=setup_app(),
                )
                entries[name] = entry
    return entries


def save_entries(entries):
    for name, entry in entries.items():
        entry.save()


def delete_entries(entries):
    for name, entry in entries.items():
        entry.delete()


if __name__ == "__main__":
    try:
        out = ccm.generate(L_CONFIG_DIR, TEMPLATE)
    except FileNotFoundError:
        out = ccm.generate(P_CONFIG_DIR, TEMPLATE)
    USER_CONFIG = out

    # print("start")
    conf = ccm.generate(USER_CONFIG, TEMPLATE)
    # devs = build_devices_from_config(conf)
    task_params = build_task_params_from_config(conf)
    entries = create_task_entries(task_params)
    print(entries)

    try:
        save_entries(entries)
        print("entries started")
        time.sleep(max(0, 60))
    except KeyboardInterrupt:
        delete_entries(entries)
        print("entries deleted")

    delete_entries(entries)
    print("done")

# dev_dict = {
#     "index": 0,
#     "device_type": "switch_low",
#     "params": {
#         "run": {"on_duration": 0.4, "unit": "seconds"},
#         "schedule": {"frequency": 2.0},
#     },
#     "fn_name": None,
#     "name": "a",
# }
