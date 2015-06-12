import numpy as np
import pylab as pl



file_in = open(sys.argv[1], "r")
name = sys.argv[2]

pairs = {}

line = file_in.readline()

tmp = line.split('-')
tmp.pop() #gets rid of \n char

for pair in tmp:
	p = pair.split(',')
	pairs[int(p[0])]=int(p[1])
#endfor

X = np.arrange(len(pairs))
pl.bar(X, pairs.values(), align='center', width=0.5)
pl.xticks(X, pairs.keys())
ymax = max(pairs.values()) + 1
pl.ylim(0, ymax)
pl.show()


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