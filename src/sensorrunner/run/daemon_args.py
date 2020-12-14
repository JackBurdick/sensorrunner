import sys
from sensorrunner.celery_app import return_worker_info
from sensorrunner.secrets import REDIS_GLOBAL_host, REDIS_GLOBAL_port, REDIS_GLOBAL_db
import redis

"""
unclear at this time why print 'works' but sys.stdout.write() does not

"""


if __name__ == "__main__":
    args = sys.argv[1:]
    config_file_path = args[0]

    try:
        r = redis.Redis(
            host=REDIS_GLOBAL_host, port=REDIS_GLOBAL_port, db=REDIS_GLOBAL_db
        )
    except Exception as e:
        sys.exit("unable to configure global redis based on secrets")

    r.set("USER_CONFIG_LOCATION", config_file_path)

    workers, worker_args = return_worker_info()

    workers_str = " ".join(workers)
    worker_args_str = " ".join(worker_args)
    CELERY_Z_OPT = f"-Z '{config_file_path}'"
    print(workers_str)
    print(worker_args_str)
    print(CELERY_Z_OPT)
    sys.exit(0)
