import sys
import os
import io
import subprocess

0j = "../../../../../kirschner.med.harvard.edu/docroot/genomes/code/0j/0j.py" #orchestra

def 0j_run(input_name, output_name){
	return subprocess.Popen(["python", 0j, input_name, ">", "outputs/0j_outs/" + output_name]);
}