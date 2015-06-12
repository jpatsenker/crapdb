import matplotlib
matplotlib.use('Agg')

import numpy as np
import pylab as pl
import sys

file_in = open(sys.argv[1], "r")

d = {}

line = file_in.readline()

tmp = line.split('-')
tmp.pop() #gets rid of \n char

for pair in tmp:
	p = pair.split(',')
	d[int(p[0])]=int(p[1])
#endfor

xs = sorted(d)
ys = []
for x in xs:
	ys.append(d[x])
#endfor


X = np.arange(len(xs))
pl.bar(X, ys, align='center', width=1)
pl.xticks(X, xs)
ymax = max(ys) + 1
pl.ylim(0, ymax)
pl.savefig(sys.argv[1] + ".png")



##OLD PLOTLY CODE DOESN"T WORK ON ORCHESTRA
#import plotly.plotly as py
#from plotly.graph_objs import *
#import io
#import os
#import sys
#import string
#
#
#
#file_in = open(sys.argv[1], "r")
#name = sys.argv[2]
#
#line = file_in.readline()
#pairs = []
#
#pairs = line.split('-')
#pairs.pop()
#
#for i in range(len(pairs)):
#	pair = pairs[i].split(',')
#	pairs[i] = pair
##endfor
#
#
#
#data = []
#data.append([])
#data.append([])
#
#for i in range(len(pairs)):
#	data[0].append(pairs[i][0])
#	data[1].append(pairs[i][1])
##endfor
#
#scat = Scatter(x=data[0], y=data[1])
#
#dat = Data([scat])
#plot_url = py.plot(dat, filename=name, world_readable=False)
#plot_url.append(".html")