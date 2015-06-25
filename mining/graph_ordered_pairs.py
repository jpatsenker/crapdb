import matplotlib

matplotlib.use('Agg')

import numpy as np
import pylab as pl
import sys

file_in = open(sys.argv[1], "r")

d = {}

line = file_in.readline()

tmp = line.split('-')
tmp.pop()  # gets rid of \n char

for pair in tmp:
    p = pair.split(',')
    d[float(p[0])] = float(p[1])

xs = sorted(d)
ys = []
for x in xs:
    ys.append(d[x])

X = np.arange(len(xs))
pl.bar(X, ys, align='edge', width=1)
pl.xticks(X, xs, rotation='vertical')
ymax = max(ys) + 1
pl.ylim(0, ymax)
pl.savefig(sys.argv[1] + ".png")
