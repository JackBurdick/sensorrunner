import importlib
import os
from pathlib import Path

import celery
from kombu import Queue

import aeropi
import crummycm as ccm
from aeropi import celeryconf
from aeropi.config.template import TEMPLATE
from aeropi.secrets import L_CONFIG_DIR, P_CONFIG_DIR
from aeropi.run.run import build_devices_from_config

path = os.path.abspath(aeropi.__file__)
o = path.split("/")[:-1]
o.append("tasks")
DEV_TASK_DIR = "/".join(o)


app = celery.Celery("celery_run")

# obtain parse config
try:
    out = ccm.generate(L_CONFIG_DIR, TEMPLATE)
except FileNotFoundError:
    out = ccm.generate(P_CONFIG_DIR, TEMPLATE)
USER_CONFIG = out


def _obtain_relevant_task_dirs(out, device_dir):
    # NOTE: I'm not sure how I want to link the name to tasks. Right now I like
    # the concept of having a separate tasks directory, but that may change such
    # that the tasks are in the devices location and only highlevel/catchall
    # tasks are in the tasks directory
    dirs = []
    device_tasks = [
        x.name for x in list(filter(lambda x: x.is_dir(), Path(device_dir).iterdir()))
    ]
    for dev_name in out.keys():
        if dev_name in device_tasks:
            dirs.append(dev_name)
    return dirs


def _return_task_modules(out, device_dir):
    relevant_dirs = _obtain_relevant_task_dirs(out, device_dir)
    dir_name = DEV_TASK_DIR.split("/")[-1]
    m_names = []
    for d in relevant_dirs:
        m_names.append(f"aeropi.{dir_name}.{d}")
    return m_names


m_names = _return_task_modules(USER_CONFIG, DEV_TASK_DIR)


def _return_queues(m_names):
    used_queues = []
    for m_name in m_names:
        cur_mod = importlib.import_module(f"{m_name}.tasks")
        cur_tasks = [
            getattr(cur_mod, o)
            for o in dir(cur_mod)
            if type(getattr(cur_mod, o)).__name__ == "PromiseProxy"
        ]
        for t in cur_tasks:
            try:
                q = t.queue
            except KeyError:
                q = None
            if q:
                if q not in used_queues:
                    used_queues.append(q)
    return used_queues


used_queues = _return_queues(m_names)
queues = [Queue(q) for q in used_queues]

# set Queues
tmp = list(celeryconf.task_queues)
tmp.extend(queues)
celeryconf.task_queues = tuple(tmp)

app.config_from_object(celeryconf)


app.autodiscover_tasks(m_names, force=True)

# aeropi/scratch/config_run/configs/basic_i2c.yml
# possibly helpful later:
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0

# DEVICES = build_devices_from_config(USER_CONFIG)
