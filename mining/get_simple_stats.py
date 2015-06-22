import sys


# CMD ARGV 1 - Input File Name
# CMD ARGV 2 - Output File Name




# Open file streams
input_file_stream = open(sys.argv[1], "r")
output_file_stream = open(sys.argv[2], "w")

line = input_file_stream.readline()

numSeq = 0

linesWithX = []
linesNoM = []

# LOOP OVER INPUT FILE, AND READ ALL LENGTHS, PUTTING IN PROPER BIN

while line:
    if line[0] == '>':
        numSeq += 1

    sequence = input_file_stream.readline()
    if sequence:
        if 'X' in sequence:
            linesWithX.append(line)
        if sequence[0] != 'M':
            linesNoM.append(line)
    line = input_file_stream.readline()
input_file_stream.close()

output_file_stream.write("Total Number of Sequences: " + str(numSeq) + "\n")

output_file_stream.write("Sequences with X's (" + str(len(linesWithX)) + "):" + '\n')

# WRITE TO FILE
for line in linesWithX:
    output_file_stream.write(line)

output_file_stream.write("Sequences that don't start with M (" + str(len(linesNoM)) + "):" + '\n')

# WRITE TO FILE
for line in linesNoM:
    output_file_stream.write(line)

output_file_stream.close()
