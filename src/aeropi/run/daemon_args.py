import sys
from aeropi.celery_app import return_worker_info
from aeropi.secrets import REDIS_GLOBAL_host, REDIS_GLOBAL_port, REDIS_GLOBAL_db
import redis

"""
unclear at this time why print 'works' but sys.stdout.write() does not

"""


def main():
    out = return_worker_info()
    print(out)
    mylist = ["a", "b", "c"]
    my_args = ["arg_a", "arg_b", "arg_c"]
    return mylist, my_args


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

    my_names, my_args = main()
    a = " ".join(my_names)
    b = " ".join(my_args)

    CELERY_Z_OPT = f"-Z '{config_file_path}'"
    print(a)
    print(b)
    print(CELERY_Z_OPT)
    sys.exit(0)
