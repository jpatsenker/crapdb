import subprocess
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

process_f_0j = subprocess.Popen(['/bin/bash', '-c',
                                         '../run_with_profile.sh -q short -o /dev/null -W 12 python calculate_complexities.py ' + infile + ' ' + outfile + ".cdhit"])
process_f_cdhit = subprocess.Popen(['/bin/bash', '-c',
                                            '../run_with_profile.sh -q short -o /dev/null -W 12 python calculate_redundancies.py ' + infile + ' ' + outfile + ".0j"])
print "Finished file " + infile + "\n"