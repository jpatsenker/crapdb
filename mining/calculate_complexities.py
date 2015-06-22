import sys
import subprocess





_0j = "../../../../../kirschner.med.harvard.edu/docroot/genomes/code/0j/0j.py"  # orchestra


def run_0j(input_name, output_name):
    return subprocess.Popen(["python", _0j, input_name, ">", "tmp/0j_out/" + output_name])


def retrieve_points_of_interest(points, output_name):
    unparsed = open('tmp/0j_out/' + output_name, "r");
    line = unparsed.readline();
    while line:
        while "|" not in line and line:
            line = unparsed.readline()

        if not line:
            break

        line = unparsed.readline()


# Main:

# points of interest (% compressability) in order to compute complexity points
poi = [.1, .2, .3, .4, .5, .6, .7, .8, .9]

# get file names as commandline arguments
file_in = sys.argv[1]
file_out = sys.argv[2]

run_0j(file_in, file_out);
