import sys
import os
import subprocess


# Accept Proteome, and run full PFAM scan on every protein

# CMD ARG 1: input file name
# CMD ARG 2: output file name
# CMD ARG 3: threshold (optional)

# PFAM
pfam_path = "/opt/Pfamscan"
pfam = "pfam_scan.pl"



def run_pfam(input_file, output_file):
    here = os.getcwd()
    os.chdir(pfam_path)
    process_pfam = subprocess.Popen([pfam, input_file, "-o", output_file])
    process_pfam.wait()
    os.chdir(here)

if len(sys.argv) < 3:
    print "Please provide atleast 2 argument: input_file output_file (threshold as second argument optional) \n"
    sys.exit(1)

input_name = sys.argv[1]
output_name = sys.argv[2]

threshold = 0.001

if len(sys.argv) == 4:
    try:
        thershold = float(sys.argv[3])
    except ValueError:
        print "Threshold must be float-castable"
        sys.exit(1)





with open(input_name, "r") as stream_input:
    line = stream_input.readline()

    while line:
        line = stream_input.readline()