import util

def main():
    # get argument
    args = util.get_args()

    # print argument
    util.print_args(args)

    # run te
    for t in range(args.num_test):
        if t % args.T == 0:
            repetita_args = util.get_repetita_args(args, t)
            print(' '.join(repetita_args))
            stdout = util.call(repetita_args)
            print(stdout)
            break


if __name__ == '__main__':
    main()
