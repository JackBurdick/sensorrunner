import sys


"""
unclear at this time why print 'works' but sys.stdout.write() does not

"""


def main():
    mylist = ["a", "b", "c"]
    my_args = ["arg_a", "arg_b", "arg_c"]
    return mylist, my_args


if __name__ == "__main__":
    args = sys.argv[1:]
    my_names, my_args = main()
    a = " ".join(my_names)
    b = " ".join(my_args)
    print(a)
    print(b)
    sys.exit(0)
