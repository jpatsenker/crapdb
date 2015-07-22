import matplotlib

matplotlib.use('Agg')

import numpy as np
import pylab as pl
import sys

cols = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'm']

streams = []
wid = float(.9)/float(len(sys.argv)-3)
# print str(len(sys.argv)-1)
# print str(1/len(sys.argv)-1)
# print str(wid)

allys = []
patches = []
bars = []

for arg in sys.argv[3:]:
    #print "Using " + arg
    streams.append(open(arg, "r"))

for i in range(len(streams)):

    #print "Working " + sys.argv[i+1]

    d = {}

    line = streams[i].read()

    tmp = line.split('\n')
    #print tmp

    for pair in tmp:
        print pair
        p = pair.split(',')
        if len(p) > 1:
            try:
                d[float(p[0])] = float(p[1])
            except ValueError:
                d[float(p[0])] = float(0)
        else:
            break
    xs = sorted(d)
    ys = []
    for x in xs:
        ys.append(d[x])

    allys.extend(ys)
    X = np.arange(len(xs))
    bars.append(pl.bar(X+wid*i, ys, align='edge', width=wid, color=cols[i%len(cols)])[0])
    pl.xticks(X, xs, rotation='vertical')
    streams[i].close()

ymax = max(allys) + 1
try:
    pl.ylim(float(sys.argv[1]), float(sys.argv[2]))
except ValueError:
    pl.ylim(0, ymax)



fig = pl.gcf()
if sys.argv[3][sys.argv[3].find(".")+1:] == "cdhit":
    pl.xlabel( "Threshold (%)" )
    pl.ylabel( "Fraction Clusters to Total Sequences" )
else:
    pl.xlabel( "% Complexity" )
    pl.ylabel( "% of Corpus" )

pl.legend(bars, sys.argv[3:])

fig.tight_layout()

pl.savefig("multi.png")
pl.show()