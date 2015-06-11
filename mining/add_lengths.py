import sys
import io
import os





input = open(sys.argv[1], "r")
temp_out = open(sys.argv[2], "w")

line = input.readline()

while line:
	if line[0] == '>':
		sequence = ''
		seq_line = input.readline()
		while not sequence or seq_line[0] != '>':
			sequence += seq_line
			seq_line = input.readline()
		#endwhile
		sequence.replace('\n', '')
		temp_out.write(line + " length: " + str(len(sequence)))
		temp_out.write(sequence)
		line = sequence[sequence.rfind('>'):]
		print "next line--"
	#endif
#endwhile

#subprocess.Popen(["mv", "tmp/withlengths", argv[1]])


input.close()
temp_out.close()