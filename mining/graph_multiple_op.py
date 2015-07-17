import matplotlib

matplotlib.use('Agg')

import numpy as np
import pylab as pl
import sys

streams = []
wid = float(1)/float(len(sys.argv)-1)
print str(len(sys.argv)-1)
print str(1/len(sys.argv)-1)
print str(wid)

allys = []

for arg in sys.argv[1:]:
    #print "Using " + arg
    streams.append(open(arg, "r"))

for i in range(len(streams)):

    #print "Working " + sys.argv[i+1]

    d = {}

    line = streams[i].read()

    tmp = line.split('-')
    tmp.pop()  # gets rid of \n char
    #print tmp

    for pair in tmp:
        p = pair.split(',')
        d[float(p[0])] = float(p[1])

    xs = sorted(d)
    ys = []
    for x in xs:
        ys.append(d[x])

    allys.extend(ys)
    X = np.arange(len(xs))
    pl.bar(X+wid*i, ys, align='edge', width=wid)
    pl.xticks(X, xs, rotation='vertical')
    streams[i].close()

ymax = max(allys) + 1
pl.ylim(0, ymax)
pl.savefig("multi.png")
pl.show()