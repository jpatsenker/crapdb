import sys
import subprocess
import os.path
import bisect

_0j = "/www/kirschner.med.harvard.edu/docroot/genomes/code/0j/0j.py"  # orchestra


def perform_bin(range_list, num):
    beg = bisect.bisect_right(range_list, num)
    if range_list[beg - 1] == num:  # Handle Perfect Hit Edge Case
        return [num, num]
    elif not beg:  # Left Edge Case
        return [None, range_list[0]]
    elif beg == len(range_list):  # Right Edge Case
        return [range_list[-1], None]
    else:
        return range_list[beg - 1:beg + 1]


def run_0j(input_name, output_name):
    # print "python " + _0j + " -scores_only " + input_name + " > " + output_name
    with open(output_name, "w") as out:
        return subprocess.Popen(["python", _0j, "-scores_only", input_name], stdout=out)


def retrieve_points_of_interest(points, input_name, output_name):
    compressed_lengths = []
    lengths = []
    with open(output_name, "r") as unparsed:
        line = unparsed.readline()
        while line:
            try:
                compressed_lengths.append(int(line.split()[1]))
            except ValueError:
                print "Incorrect Parse of 0j out file"
                exit(1)
            line = unparsed.readline()
    with open(input_name, "r") as stream_in:
        line = stream_in.readline()
        while line:
            if line[0] == ">":
                try:
                    lengths.append(int(line[line.rfind("length=") + 7:-1]))
                except ValueError:
                    print "Incorrect Parse of lengths"
                    exit(1)
    compression_ratios = []
    for i in range(len(lengths)):
        compression_ratios.append(compressed_lengths[i] / lengths[i])

    binned_data = {}
    for ratio in compression_ratios:
        bin_ratio = perform_bin(points, ratio)
        try:
            binned_data[bin_ratio] += 1
        except KeyError:
            binned_data[bin_ratio] = 1

    return binned_data

# Main:

# points of interest (% compressability) in order to compute complexity points
poi = [.1, .2, .3, .4, .5, .6, .7, .8, .9]

# get file names as commandline arguments
file_in = sys.argv[1]
file_out = sys.argv[2]

process_run_0j = run_0j(file_in, "tmp/0j_out/" + os.path.basename(file_out))
process_run_0j.wait()
data = retrieve_points_of_interest(poi, file_in, "tmp/0j_out/" + os.path.basename(file_out))

with open(file_out, "w") as stream_out:
    for key, value in data:
        stream_out.write(key + "," + value + "-")
    stream_out.write("\n")