import sys
import io
import os
import subprocess


#CMD ARGV 1 - Input File Name
#CMD ARGV 2 - Output File Name
#CMD ARGV 3 - Bin Size in amino acids




#get histogram bin size
bin_size = 0
try:
	bin_size = int(sys.argv[3])
except ValueError:
	print "NO!!!!!"
	sys.exit(0)

#Open file streams
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")

line = input.readline()

#this will hold the histogram
lengths = {}

#LOOP OVER INPUT FILE, AND READ ALL LENGTHS, INCREMENTING FOR EACH LENGTH

while line:
	while line and line[0]!='>':
		line = input.readline()
		print "hi"
	#endwhile
	if not line:
		break
	#endif
	print line
	l = int(line[line.rfind("length=")+7:-1])/bin_size

	if l in lengths:
		lengths[l]+=1
	else:
		lengths[l] = 1
	#endif
	line = input.readline()
#endwhile
input.close()

#WRITE TO FILE
for key in lengths:
	output.write(str(key*bin_size) + "," + str(lengths[key]) + "-")
#endfor
output.close()