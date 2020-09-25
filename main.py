import util

def main():
    # get argument
    args = util.get_args()

    # print argument
    util.print_args(args)

    # get repetita args
    args = util.get_repetita_args(args, 0)
    print(args)
    stdout = util.call(args)
    print(stdout)


if __name__ == '__main__':
    main()
