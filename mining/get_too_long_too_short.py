import sys
import io
import os
import subprocess


# CMD ARGV 1 - Input File Name
# CMD ARGV 2 - Output File Name
# CMD ARGV 3 - Too Short
# CMD ARGV 4 - Too Long


lowlim = 0
highlim = 0

try:
    lowlim = int(sys.argv[3])
    highlim = int(sys.argv[4])
except ValueError:
    print "Improper type supplied as limits"
    sys.exit(0)

# Open file streams
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")

line = input.readline()

too_short = []
too_long = []

# LOOP OVER INPUT FILE, AND READ ALL LENGTHS, PUTTING IN PROPER BIN

while line:
    if line[0] == '>':
        try:
            l = int(line[line.rfind("length=") + 7:-1])
        except ValueError:
            print "Improper lengths set up in file"
            sys.exit(0)
        if l < lowlim:
            too_short.append(line)
        elif l > highlim:
            too_long.append(line)

    line = input.readline()
input.close()

output.write("Sequences that are too short (" + str(len(too_short)) + "):" + '\n')

# WRITE TO FILE
for so_short in too_short:
    output.write(so_short)

output.write("Sequences that are too long (" + str(len(too_long)) + "):" + '\n')

# WRITE TO FILE
for so_long in too_long:
    output.write(so_long)
output.close()
