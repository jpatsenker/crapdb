import sys
import os
import numbers
import io




#Main

#Map that will hold all values

protein_dictionary = {}
file_in_name = sys.argv[1]
file_in = open(file_in_name, "r")

if "/" in file_in_name:
	file_in_name = file_in_name[(file_in_name.rfind("/")+1):file_in_name.rfind(".")]
#endif

file_out = open("inputs/" + file_in_name + "_LT.fasta", "w");

line = file_in.readline()

while line:
	gene_id = line[1:line.find("|")]
	transcript_length = line[(line.rfind("|")+1):]
	print "READING: " + gene_id
	if gene_id in protein_dictionary:
		if not isinstance(transcript_length, numbers.Integral):
			protein_dictionary[gene_id] = 0
		elif protein_dictionary[gene_id]>transcript_length:
			protein_dictionary[gene_id] = transcript_length
		#endif
	else:
		if not isinstance(transcript_length, numbers.Integral):
			protein_dictionary[gene_id] = 0
		else:
			protein_dictionary[gene_id] = transcript_length
		#endif
	#endif

	line = file_in.readline()
	if line:
		while line[0]!='>':
			line = file_in.readline()
			if not line:
				break
			#endif
		#endwhile
	#endif
#endwhile

file_in.seek(0,0)

line = file_in.readline()

while line:
	gene_id = line[1:line.find("|")]
	transcript_length = line[(line.rfind("|")+1):]
	if not isinstance(transcript_length, numbers.Integral):
		transcript_length = 0
	#endif
	write = 0
	if protein_dictionary[gene_id] == transcript_length:
		write = 1
		print "WRITING: " + gene_id
	#endif
	if write:
		file_out.write(line)
	#endif
	line = file_in.readline()
	if line:
		while line[0]!='>':
			if write:
				file_out.write(line)
			#endif
			line = file_in.readline()
			if not line:
				break
		#endwhile
	#endif
#endwhile

close(file_in)
close(file_out)