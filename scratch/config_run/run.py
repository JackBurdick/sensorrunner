from sensorrunner.user_config import USER_CONFIG
import celery
from redbeat import RedBeatSchedulerEntry as Entry

import time
from sensorrunner.celery_app import setup_app
from sensorrunner.run.run import (
    build_task_params_from_config,
)

app = setup_app()


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
                    app=app,
                )
                entries[name] = entry
    return entries


def save_entries(entries):
    for name, entry in entries.items():
        entry.save()


def delete_entries(entries):
    for name, entry in entries.items():
        entry.delete()
    # TODO: turn off devices


if __name__ == "__main__":
    task_params = build_task_params_from_config(USER_CONFIG)
    entries = create_task_entries(task_params)
    print(entries)

    try:
        save_entries(entries)
        print("entries started")
        time.sleep(max(0, 600))
    except KeyboardInterrupt:
        delete_entries(entries)
        print("entries deleted")

    delete_entries(entries)
    # TODO: allow to finish?
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
