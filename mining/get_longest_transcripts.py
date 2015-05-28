import sys
import os




#Main

#Map that will hold all values

protein_dictionary = {}
file_in_name = sys.argv[1]
file_in = open(file_in_name, "r")

if "/" in file_in_name:
	file_in_name = file_in_name[file_in_name.rfind("/"):file_in_name.rfind(".")]
#endif

file_out = open("inputs/" + file_in_name + "_LT.fasta");

line = file_in.readline()

while line:
	
	gene_id = line[1:line.find("|")]
	transcript_length = line[line.rfind("|"):]
	
	if protein_dictionary[gene_id]:
		if protein_dictionary[gene_id]>transcript_length:
			protein_dictionary[gene_id] = transcript_length
		#endif
	#endif

	while line[0]!='>':
		line = file_in.readline()
	#endwhile

#endwhile

file_in.seek(0,0)

line = file_in.readline()

while line:
	gene_id = line[1:line.find("|")]
	transcript_length = line[line.rfind("|"):]

	write = 0

	if protein_dictionary[gene_id] == transcript_length:
		write = 1
	#endif

	while line[0]!='>':
		if write:
			file_out.write(line)
		#endif
		line = file_in.readline()
	#endwhile



#endwhile

close(file_in)
close(file_out)