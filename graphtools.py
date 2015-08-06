import matplotlib

matplotlib.use('Agg')

import numpy as np
import pylab as pl


def graph_histogram(dict_in, x_lab, y_lab, save_file):
    np.array(dict_in.items())
    pl.hist(, 50, normed=1, facecolor='green', alpha=0.75)
    pl.xlabel(x_lab)
    pl.ylabel(y_lab)
    pl.savefig(save_file)