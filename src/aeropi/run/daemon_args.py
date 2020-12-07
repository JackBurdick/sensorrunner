import sys
from aeropi.celery_app import return_worker_info

"""
unclear at this time why print 'works' but sys.stdout.write() does not

"""


def main(config_location):
    out = return_worker_info(config_location=config_location)
    print(out)
    mylist = ["a", "b", "c"]
    my_args = ["arg_a", "arg_b", "arg_c"]
    return mylist, my_args


if __name__ == "__main__":
    args = sys.argv[1:]
    config_location = args[0]
    my_names, my_args = main(config_location)
    a = " ".join(my_names)
    b = " ".join(my_args)

    CELERY_Z_OPT = f"-Z '{config_location}'"
    print(a)
    print(b)
    print(CELERY_Z_OPT)
    sys.exit(0)
