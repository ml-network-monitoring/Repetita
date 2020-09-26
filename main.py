import util
import re

def parse_routing(t, args):
    N_dict = {'abilene_tm': 12, 'geant_tm': 30, 'brain_tm': 9}
    N = N_dict[args.dataset]
    routing = [[[] for i in range(N)] for j in range(N)]
    routing_txt = open('../result/{}/routing.{}.txt'.format(args.dataset, t)).read()

    flag = False
    for line in routing_txt.split('\n'):
        if 'sr paths' in line:
            flag = True
        if flag:
            if 'Destination' in line:
                i = int(re.findall('(\d+)_', line)[0])
            if 'sequence of middlepoints:' in line:
                nodes = [int(_) for _ in re.findall('(\d+)_', line)]
                j = nodes[0]
                k = nodes[1:]
                routing[i][j] = k
        if 'ecmp paths' in line:
            break
    return routing

def parse_result(t, stdout, args):
    mlus = []
    rc = None
    # parse mlu
    mlus = re.findall(r'max link utilization\:\s+(\d+\.\d+)', stdout)
    mlus = [float(mlu) for mlu in mlus]
    # parse rc
    if t >= args.T + 1:
        prev_routing = open('../result/{}/routing.{}.txt'.format(args.dataset, t)).read()
        routing      = open('../result/{}/routing.{}.txt'.format(args.dataset, t)).read()
        print(prev_routing)
    return mlus, rc

def main():
    # get argument
    args = util.get_args()

    # print argument
    util.print_args(args)

    # run te
    for t in range(args.num_test):
        if t % (args.T + 1) == 0:
            repetita_args = util.get_repetita_args(args, t)
            stdout = util.call(repetita_args)
            print(stdout)
            parse_result(t, stdout, args)
            if t > args.T + 1:
                break


if __name__ == '__main__':
    main()
