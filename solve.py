import re

N = 12 # if else thoi
routing = [[[] for i in range(N)] for j in range(N)]
routing_txt = open('../result/abilene_tm/routing.0.txt').read()

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

