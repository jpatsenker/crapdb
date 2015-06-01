import sys
import os
import io
import subprocess

0j = "../../../../../kirschner.med.harvard.edu/docroot/genomes/code/0j/0j.py" #orchestra

def 0j_run(input_name, output_name):
	return subprocess.Popen(["python", 0j, input_name, ">", "tmp/0j_out/" + output_name])
#enddef

def retrieve_points_of_interest(points, output_name):
	unparsed = open("tmp/0j_out/" + output_name, "r");
	line = unparsed.readline();
	while line:
	
	#endwhile


#enddef







#Main:

#points of interest (% compressability) in order to compute complexity points
poi = [.1, .2, .3, .4, .5, .6, .7, .8, .9]

#get filenames as commandline arguments
file_in = sys.argv[1]
file_out = sys.argv[2]

0j_run(input_name, output_name);


