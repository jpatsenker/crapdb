import plotly.plotly as py
from plotly.graph_objs import *
import io
import os
import sys
import string



file_in = open(sys.argv[1], "r")

line = file_in.readline()
pairs = []

pairs = line.split('-')
pairs.pop()

for i in range(len(pairs)):
	pair = pairs[i].split(',')
	pairs[i] = pair
#endfor



data = []
data.append([])
data.append([])

for i in range(len(pairs)):
	data[0].append(pairs[i][0])
	data[1].append(pairs[i][1])
#endfor

scat = Scatter(x=data[0], y=data[1])

dat = Data([scat])
plot_url = py.plot(dat, filename='basic-line', world_readable=False)
plot_url.append(".html")