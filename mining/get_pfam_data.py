from os.path import basename
import sys
import subprocess


# Accept Proteome, and run full PFAM scan on every protein

# CMD ARG 1: input file name
# CMD ARG 2: output file name
# CMD ARG 3: threshold (optional)

# PFAM
pfam_path = "/opt/Pfamscan"
pfam = "pfam_scan.pl"


def run_pfam(input_file, output_file):
    # process_pfam = subprocess.Popen(
    #     ["/bin/bash", "-c", "../run_with_profile.sh -q long -K -W 1 " + pfam + "-fasta" + input_file + "-o" + output_file])
    # process_pfam.wait()
    print "run"


if len(sys.argv) < 3:
    print "Please provide atleast 2 argument: input_file output_file (threshold as second argument optional) \n"
    sys.exit(1)

input_name = sys.argv[1]
output_name = sys.argv[2]

threshold = 0.001

tmp_dir = "tmp/"
count = 0

if len(sys.argv) == 4:
    try:
        thershold = float(sys.argv[3])
    except ValueError:
        print "Threshold must be float-castable"
        sys.exit(1)

with open(input_name, "r") as stream_input:
    line = stream_input.readline()

    i = 0

    # Break into tmp files
    while line:
        if line[0] == ">":
            sequence = stream_input.readline()
            if sequence:
                with open(tmp_dir + basename(input_name) + "_" + str(count), "a") as stream_tmp:
                    stream_tmp.write(line)
                    stream_tmp.write(sequence)
            else:
                break

            if i == 20:
                i = 0
                count += 1
            else:
                i += 1

        line = stream_input.readline()

for fileNum in range(count):
    run_pfam(tmp_dir + basename(input_name) + "_" + str(fileNum),
             tmp_dir + "pfam_out_" + basename(input_name) + "_" + str(fileNum))
