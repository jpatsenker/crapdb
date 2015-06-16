import sys
import io
import os
import subprocess


#CMD ARGV 1 - Input File Name
#CMD ARGV 2 - Output File Name
#CMD ARGV 3 - Too Short
#CMD ARGV 4 - Too Long


lowlim = 0
highlim = 0

try:
	lowlim = int(sys.argv[3])
	highlim = int(sys.argv[4])
except ValueError:
	print "NO!!!!!"
	sys.exit(0)
#endtry

#Open file streams
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")

line = input.readline()

too_short = []
too_long = []

#LOOP OVER INPUT FILE, AND READ ALL LENGTHS, PUTTING IN PROPER BIN

while line:
	if line[0]=='>':
		try:
			l = int(line[line.rfind("length=")+7:-1])
		except ValueError:
			print "NO!!!!"
			sys.exit(0)
		#endtry
		if l < lowlim:
			too_short.append(line)
		elif l > highlim:
			too_long.append(line)
	#endif
#endif
line = input.readline()
#endwhile
input.close()


output.write("Sequences that are too short (" + len(too_short) + ": ")

#WRITE TO FILE
for short in too_short:
	output.write(short)
#endfor

output.write("Sequences that are too long (" + len(too_long) + ": ")

#WRITE TO FILE
for long in too_long:
	output.write(long)
#endfor
output.close()
