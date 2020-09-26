import util

def main():
    # get argument
    args = util.get_args()

    # print argument
    util.print_args(args)

    # at every T + 1 step
    t = 1995
    repetita_args = util.get_repetita_args(args, t)
    print('command:', ' '.join(repetita_args))
    stdout = util.call(repetita_args)
    print('stdout:', stdout)


if __name__ == '__main__':
    main()
