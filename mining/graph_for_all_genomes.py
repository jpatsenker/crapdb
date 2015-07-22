import sys
import os
import matplotlib

matplotlib.use('Agg')

import numpy as np
import pylab as pl

poi = 0
direc = ""
outfile = ""
files = []

try:
    direc = sys.argv[1]
except IndexError:
    print "Improper Parameter: missing directory"
    exit(1)

try:
    files = os.listdir(direc)
except OSError:
    print "Improper Parameter: directory does not exist"
    exit(1)

try:
    outfile = sys.argv[2]
except IndexError:
    print "Improper Parameter: missing out-file"
    exit(1)

try:
    poi = sys.argv[3]
except IndexError:
    print "Improper Parameter: missing % of interest"
    exit(1)

try:
    poi = float(poi)
except ValueError:
    print "Improper Parameter: % of interest must be a float"
    exit(1)

d = {}

for f in files:
    if f[f.rfind("."):] == ".0j" or f[f.rfind("."):] == ".cdhit":
        with open(direc + f) as stream_f:
            everything = stream_f.read()
            pairs = everything.split("\n")
            pairs.pop() #rid of last empty pair
            for pair in pairs:
                ord_pair = pair.split(",")
                try:
                    if float(ord_pair[0]) == poi:
                        d[f] = float(ord_pair[1])
                        print f + " " + d[f] + "\n"
                except (IndexError, ValueError):
                    print "Improperly Formatted File"
                    exit(1)

xs = d.keys()
ys = d.values()

X = np.arange(len(xs))
pl.bar(X, ys, align = 'edge')
pl.xticks(X, xs, rotation='vertical')

pl.ylim(0,.4)
pl.savefig(outfile)
pl.show()