import sys




# Main

# Map that will hold all values

protein_dictionary = {}
file_in_name = sys.argv[1]
file_in = open(file_in_name, "r")

if "/" in file_in_name:
    file_in_name = file_in_name[(file_in_name.rfind("/") + 1):file_in_name.rfind(".")]

file_out = open("inputs/" + file_in_name + "_LT.fasta", "w");

line = file_in.readline()

while line:
    gene_id = line[1:line.find("|")]
    transcript_length = line[(line.rfind("|") + 1):-1]
    # print "READING: " + gene_id
    if gene_id in protein_dictionary:
        if not unicode(transcript_length, "utf-8").isnumeric():
            protein_dictionary[gene_id] = 0
        elif protein_dictionary[gene_id] > transcript_length:
            protein_dictionary[gene_id] = transcript_length
    else:
        print "check"
        if not unicode(transcript_length, "utf-8").isnumeric():
            print str(transcript_length)
            protein_dictionary[gene_id] = 0
        else:
            protein_dictionary[gene_id] = transcript_length

    line = file_in.readline()
    if line:
        while line[0] != '>':
            line = file_in.readline()
            if not line:
                break

file_in.seek(0, 0)

line = file_in.readline()

while line:
    gene_id = line[1:line.find("|")]
    transcript_length = line[(line.rfind("|") + 1):-1]
    if not unicode(transcript_length, "utf-8").isnumeric():
        transcript_length = 0
    write = 0
    if protein_dictionary[gene_id] == transcript_length:
        write = 1
    # print "WRITING: " + gene_id
    if write:
        file_out.write(line)
    line = file_in.readline()
    if line:
        while line[0] != '>':
            if write:
                file_out.write(line)
            line = file_in.readline()
            if not line:
                break

file_in.close()
file_out.close()
