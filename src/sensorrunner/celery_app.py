import importlib
import os
import sys
from pathlib import Path

import celery
from celery import signals
from click import Option
from kombu import Queue

import sensorrunner
import crummycm as ccm
from sensorrunner import celeryconf
from sensorrunner.config.template import TEMPLATE
from sensorrunner.secrets import REDIS_GLOBAL_host, REDIS_GLOBAL_port, REDIS_GLOBAL_db
import redis

importlib.reload(sensorrunner)

# from sensorrunner.run.run import build_devices_from_config

path = os.path.abspath(sensorrunner.__file__)
o = path.split("/")[:-1]
o.extend(["tasks", "devices"])
DEV_TASK_DIR = "/".join(o)


app = celery.Celery("celery_run")
app.config_from_object(celeryconf)

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
        config_file_path = options["device_config"]
    except KeyError:
        sys.exit("--device_config (-Z) was not included passed")
    if config_file_path is None:
        sys.exit("--device_config (-Z) is set to None, but is expected to be a path")
    if not isinstance(config_file_path, str):
        sys.exit(
            f"--device_config (-Z) ({config_file_path}) expected to be {str} not {type(config_file_path)}"
        )
    if not Path(config_file_path).is_file():
        sys.exit(
            f"--device_config (-Z) is not a valid file {config_file_path}, maybe try absolute location"
        )

    try:
        r = redis.Redis(
            host=REDIS_GLOBAL_host, port=REDIS_GLOBAL_port, db=REDIS_GLOBAL_db
        )
    except Exception as e:
        sys.exit("unable to configure global redis based on secrets")

    r.set("USER_CONFIG_LOCATION", config_file_path)
    _ = setup_app()


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
        m_names.append(f"sensorrunner.{dir_name}.{d}")
    return m_names


def _return_queues(m_names):
    used_queues = []
    for m_name in m_names:
        try:
            cur_mod = importlib.import_module(f"{m_name}.tasks")
        except ModuleNotFoundError as e:
            sys.exit(f"module {m_name} not found: {e}")
        cur_tasks = [
            getattr(cur_mod, o)
            for o in dir(cur_mod)
            if type(getattr(cur_mod, o)).__name__ == "PromiseProxy"
        ]
        if cur_tasks:
            for t in cur_tasks:
                try:
                    q = t.queue
                except KeyError:
                    q = None
                if q:
                    if q not in used_queues:
                        used_queues.append(q)
    return used_queues


def return_worker_info():
    r = redis.Redis(host=REDIS_GLOBAL_host, port=REDIS_GLOBAL_port, db=REDIS_GLOBAL_db)
    config_location = r.get("USER_CONFIG_LOCATION").decode("utf-8")
    if not config_location:
        sys.exit("config_location not found in database")
    user_config = ccm.generate(config_location, TEMPLATE)
    if not user_config:
        sys.exit("user_config is empty")
    m_names = _return_task_modules(user_config, DEV_TASK_DIR)
    used_queues = _return_queues(m_names)

    # NOTE: `collect` is a 'magic queue' that is, it is special compared to all
    # other queues.
    # TODO: this logic should be generalized a bit more in the future
    MAGIC_QUEUES = {"collect": "-Q:main 'collect' -c:main 3"}
    workers, worker_args = [], []
    for qname in used_queues:
        worker_name = f"{qname}_worker"
        if qname not in MAGIC_QUEUES:
            worker_arg = f"-Q:{worker_name} '{qname}' -c:{worker_name} 1"
        else:
            worker_arg = MAGIC_QUEUES[qname]
        workers.append(worker_name)
        worker_args.append(worker_arg)
    return (workers, worker_args)


def setup_app():
    r = redis.Redis(host=REDIS_GLOBAL_host, port=REDIS_GLOBAL_port, db=REDIS_GLOBAL_db)
    config_location = r.get("USER_CONFIG_LOCATION").decode("utf-8")
    if not config_location:
        sys.exit("config_location not found in database")
    user_config = ccm.generate(config_location, TEMPLATE)
    if not user_config:
        sys.exit("user_config empty")

    # Create relevant queues
    m_names = _return_task_modules(user_config, DEV_TASK_DIR)
    used_queues = _return_queues(m_names)
    queues = [Queue(q) for q in used_queues]

    # Set Queues
    tmp = list(celeryconf.task_queues)
    tmp.extend(queues)
    celeryconf.task_queues = tuple(tmp)

    # attempt to force when adding new queues
    app.autodiscover_tasks(m_names, force=True)
    return app


# sensorrunner/scratch/config_run/configs/basic_i2c.yml
# possibly helpful later:
# https://gist.github.com/chenjianjx/53d8c2317f6023dc2fa0
