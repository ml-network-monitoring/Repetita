import os
import argparse

def get_args():
    # create argument parser
    parser = argparse.ArgumentParser()

    # parameter for dataset
    parser.add_argument('--dataset', type=str, default='abilene_tm',
                        choices=['abilene_tm', 'geant_tm', 'brain_tm'])
    parser.add_argument('--T', type=int, default=6)
    parser.add_argument('--num_test', type=int, default=2000)

    # parameter for solver
    parser.add_argument('--solver', type=str, default='MIPTwoSRNoSplit',
                        choices=['MIPTwoSRNoSplit'])

    # parameter for scenario
    parser.add_argument('--scenario', type=str, default='MultiStepSolverRun',
                        choices=['MultiStepSolverRun'])
    # get args
    args = parser.parse_args()

    # append other constants
    args.repetita_home = os.getcwd()
    args.home = os.path.join(os.path.dirname(args.repetita_home), 'code')

    return args

def print_args(args):
    print('---------------------------------------')
    print('--------------REPETITA-----------------')
    print('---------------------------------------')
    print('    - dataset       :', args.dataset)
    print('    - solver        :', args.solver)
    print('    - scenario      :', args.scenario)
    print('---------------------------------------')
    print('    - home          :', args.home)
    print('    - repetita_home :', args.repetita_home)
    print('---------------------------------------')

def get_repetita_args(args, t):
    args = ['./repetita',
            '-graph',
            os.path.join(args.home,
                         'topo',
                         '{}.graph'.format(args.dataset)),
            '-demands',
            os.path.join(args.home,
                         'data',
                         '{}.{}.demands'.format(args.dataset, t)),
            '-demandchanges',
            '  '.join([os.path.join(args.home,
                         'data',
                         '{}.{}.demands'.format(args.dataset, t + i)) for i in range(1, args.T + 1)]),
            '-solver',
            args.solver,
            '-scenario',
            args.scenario,
            '-outpaths',
            'out.txt'
            ]
    return args
