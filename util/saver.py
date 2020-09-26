import os
import numpy as np

solver_dict = {'MIPTwoSRNoSplit': 'mip2sr', 'SRLS': 'srls'}

def save(mlus, rcs, args):
    # convert to numpy
    mlus = np.array(mlus)
    rcs = np.array(rcs)

    # make folder if needed
    folder = '../summary'
    if not os.path.exists(folder):
        os.mkdir(folder)
    folder = os.path.join(folder, args.dataset)
    if not os.path.exists(folder):
        os.mkdir(folder)

    # construct filename
    prefix = '{}/last_step_{}'.format(folder, solver_dict[args.solver])
    np.save('{}_mlu'.format(prefix), mlus)
    np.save('{}_rc'.format(prefix), rcs)

