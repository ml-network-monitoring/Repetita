import util

def main():
    # get argument
    args = util.get_args()

    # print argument
    util.print_args(args)

    # run te
    mlus = []
    rcs = []

    # at every T + 1 step
    for t in range(args.num_test):
        if t % (args.T + 1) == 0:

            repetita_args = util.get_repetita_args(args, t)
            stdout = util.call(repetita_args)
            mlu, rc = util.parse_result(t, stdout, args)
            mlus.append(mlu)
            if rc is not None:
                rcs.append(rc)

        if t > 30:
            break

    util.save(mlus, rcs, args)

if __name__ == '__main__':
    main()
