import sys
import io
import os





input = open(sys.argv[1], "r")
temp_out = open(sys.argv[2], "w")

line = input.readline()

while line:
	if line[0] == '-':
		break
	#endif

	if line[0] == '>':
		sequence = ''
		seq_line = input.readline()
		while seq_line and seq_line[0] != '>' and seq_line[0] != '-':
			sequence += seq_line
			seq_line = input.readline()
		#endwhile
		sequence = sequence.replace('\n', '')
		print sequence
		temp_out.write(line[:-1] + " length=" + str(len(sequence)) + '\n')
		temp_out.write(sequence)
		line = seq_line
	else:
		line = input.readline()
	#endif
#endwhile

#subprocess.Popen(["mv", "tmp/withlengths", argv[1]])


input.close()
temp_out.close()