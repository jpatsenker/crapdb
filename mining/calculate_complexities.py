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


def retrieve_points_of_interest(points, output_name):
    compressed_lengths = []
    lengths = []
    with open(output_name, "r") as unparsed:
        line = unparsed.readline()
        while line:
            try:
                compressed_lengths.append(int(line.split()[1]) - int(line.split()[2]))
                lengths.append(int(line.split()[1]))
            except ValueError:
                print "Incorrect Parse of 0j out file"
                exit(1)
            line = unparsed.readline()

    compression_ratios = []
    for i in range(len(lengths)):
        compression_ratios.append(float(compressed_lengths[i]) / float(lengths[i]))

    binned_data = {}
    for ratio in compression_ratios:
        print str(ratio) + "\n"
        bin_ratio = perform_bin(points, ratio)
        print str(bin_ratio) + "\n"
        try:
            binned_data[bin_ratio[0]] += 1
        except KeyError:
            binned_data[bin_ratio[0]] = 1

    return binned_data

def get_total_num_seq(stream_infile):
    num = 0
    line = stream_infile.readline()
    while line:
        num += 1
        line = stream_infile.readline()
    return num/2
# Main:

# points of interest (% compressability) in order to compute complexity points
poi = [0, .05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .85, .9, .95, 1.00]

# get file names as commandline arguments
file_in = sys.argv[1]
file_out = sys.argv[2]

total = 0

with open(file_in, "r") as stream_in:
    total = get_total_num_seq(stream_in)

process_run_0j = run_0j(file_in, "tmp/0j_out/" + os.path.basename(file_out))
process_run_0j.wait()
data = retrieve_points_of_interest(poi, "tmp/0j_out/" + os.path.basename(file_out))

with open(file_out, "w") as stream_out:
    for p in poi:
        try:
            stream_out.write(str(p) + "," + str(float(data[p])/float(total)))
        except KeyError:
            stream_out.write(str(p) + ",0")
        stream_out.write("\n")