import util

def main():
    # get argument
    args = util.get_args()

    # print argument
    util.print_args(args)

    # run te
    mlus = []
    rcs = []

    # at every T step
    for t in range(args.num_test):
        if t % args.T == 0:
            repetita_args = util.get_repetita_args(args, t)
            print('command:', ' '.join(repetita_args))
            stdout = util.call(repetita_args)
            if stdout:
                print('stdout:', stdout)
                mlu, rc = util.parse_result(t, stdout, args)
                if len(mlu) == args.T:
                    mlus.append(mlu)
                if rc is not None:
                    rcs.append(rc)

    util.save(mlus, rcs, args)

if __name__ == '__main__':
    main()
