import importlib
import os
import sys
from pathlib import Path

import celery
from celery import signals
from click import Option
from kombu import Queue

import aeropi
import crummycm as ccm
from aeropi import celeryconf
from aeropi.config.template import TEMPLATE

importlib.reload(aeropi)

# from aeropi.run.run import build_devices_from_config

path = os.path.abspath(aeropi.__file__)
o = path.split("/")[:-1]
o.extend(["tasks", "devices"])
DEV_TASK_DIR = "/".join(o)


app = celery.Celery("celery_run")


app.user_options["preload"].add(
    Option(
        ("-Z", "--device_config"), default=None, help="location of device configuration"
    )
)


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    if not options:
        sys.exit("no options exist, but --device_config (-Z) is required")
    try:
        confg_file_path = options["device_config"]
    except KeyError:
        sys.exit("--device_config (-Z) was not included passed")
    if confg_file_path is None:
        sys.exit("--device_config (-Z) is set to None, but is expected to be a path")
    if not isinstance(confg_file_path, str):
        sys.exit(
            f"--device_config (-Z) ({confg_file_path}) expected to be {str} not {type(confg_file_path)}"
        )
    if not Path(confg_file_path).is_file():
        sys.exit(
            f"--device_config (-Z) is not a valid file {confg_file_path}, maybe try absolute location"
        )
    USER_CONFIG = ccm.generate(confg_file_path, TEMPLATE)
    setup_app(USER_CONFIG, DEV_TASK_DIR, celeryconf)


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
    # TODO: more robust logic
    dir_name = device_dir.split("/")[-2:]
    dir_name = ".".join(dir_name)
    m_names = []
    for d in relevant_dirs:
        m_names.append(f"aeropi.{dir_name}.{d}")
    return m_names


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


def setup_app(USER_CONFIG, DEV_TASK_DIR, celeryconf):
    # Create relevant queues
    m_names = _return_task_modules(USER_CONFIG, DEV_TASK_DIR)
    used_queues = _return_queues(m_names)
    queues = [Queue(q) for q in used_queues]

    # Set Queues
    tmp = list(celeryconf.task_queues)
    tmp.extend(queues)
    celeryconf.task_queues = tuple(tmp)

    # attempt to force when adding new queues
    app.config_from_object(celeryconf)
    app.autodiscover_tasks(m_names, force=True)


# aeropi/scratch/config_run/configs/basic_i2c.yml
# possibly helpful later:
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0
