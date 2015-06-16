import sys
import io
import os
import subprocess


#CMD ARGV 1 - Input File Name
#CMD ARGV 2 - Output File Name




#Open file streams
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")

line = input.readline()

numSeq = 0

linesWithX = []
linesNoM = []

#LOOP OVER INPUT FILE, AND READ ALL LENGTHS, PUTTING IN PROPER BIN

while line:
	if line[0]=='>':
		numSeq+=1

	#endif
	sequence = input.readline()
	if sequence:
		if 'X' in sequence:
			linesWithX.append(line)
		#endif
		if sequence[0] != 'M':
			linesNoM.append(line)
		#endif
	#endif
	line = input.readline()
#endwhile
input.close()


output.write("Total Number of Sequences: " + str(numSeq) + "\n")

output.write("Sequences with X's (" + str(len(linesWithX)) + "):" + '\n')

#WRITE TO FILE
for line in linesWithX:
	output.write(line)
#endfor

output.write("Sequences that don't start with M (" + str(len(linesNoM)) + "):" + '\n')

#WRITE TO FILE
for line in linesNoM:
	output.write(line)
#endfor



output.close()
