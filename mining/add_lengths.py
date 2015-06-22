import sys

file_input_stream = open(sys.argv[1], "r")
temp_out = open(sys.argv[2], "w")

line = file_input_stream.readline()

while line:
    if line[0] == '-':
        break
    # endif

    if line[0] == '>':
        sequence = ''
        seq_line = file_input_stream.readline()
        while seq_line and seq_line[0] != '>' and seq_line[0] != '-':
            sequence += seq_line
            seq_line = file_input_stream.readline()
        sequence = sequence.replace('\n', '')
        temp_out.write(line[:-1] + " length=" + str(len(sequence)) + '\n')
        temp_out.write(sequence + '\n')
        line = seq_line
    else:
        line = file_input_stream.readline()

file_input_stream.close()
temp_out.close()
