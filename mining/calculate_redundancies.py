import sys
import io
import os
import subprocess

cdhit = "/opt/cd-hit/bin/cd-hit" #orchestra
#cdhit = "../../../cd-hit/cd-hit" #local

def cd_hit_run(input_name, output_name, threshold):
	return subprocess.Popen([cdhit, "-i", input_name, "-o", output_name, "-c", str(threshold)])
#enddef

def count_non_redundant_seq(out_file):
	nr = 0
	out = open(out_file, "r")
	line = out.readline()
	while line:
		if line[0] == '>':
			nr+=1
		#endif
		line = out.readline()
	#endwhile
	return nr
#enddef




#Main


#All thresholds to run CD-HIT on
	#Don't run on anything lower than .7 or cluster may crash

tholds = [.7, .8, .9]
file_in = sys.argv[1]
fout = open("outputs/cdhit_outs", "w")



for i in range(len(tholds)):
	p1 = cd_hit_run(file_in, "tmp/out", tholds[i])
	p1.wait()
	result = count_non_redundant_seq("tmp/out")
	fout(result)
#endfor


file_in.close()
fout.close()