import re

N_dict = {'abilene_tm': 12, 'geant_tm': 30, 'brain_tm': 9}

def parse_routing(t, args):
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

def get_rc(prev_routing, routing, args):
    N = N_dict[args.dataset]
    rc = 0
    for i in range(N):
        for j in range(N):
            if prev_routing[i][j] != routing[i][j]:
                rc += 1
    return rc


def parse_result(t, stdout, args):
    mlus = []
    rc = None
    # parse mlu
    mlus = re.findall(r'max link utilization\:\s+(\d+\.\d+)', stdout)
    mlus = [float(mlu) for mlu in mlus]
    # parse rc
    if t >= args.T + 1:
        prev_routing = parse_routing(t - args.T - 1, args)
        routing = parse_routing(t, args)
        rc = get_rc(prev_routing, routing, args)
    return mlus, rc

