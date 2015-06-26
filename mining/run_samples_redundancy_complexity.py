import os
import subprocess

files = os.listdir("inputs/sample/")




for f in files:
    if f != "empty_file_for_git":
        process_f_0j = subprocess.Popen(['/bin/bash', '-c', '../run_with_profile.sh -q short -K -W 12 python calculate_complexities.py inputs/sample/' + f + ' outputs/0j_out/sample'])
        process_f_cdhit = subprocess.Popen(['/bin/bash', '-c', '../run_with_profile.sh -q short -K -W 12 python calculate_redundancies.py inputs/sample/' + f + ' outputs/cdhit_out/sample'])
        print "Finished file " + f + "\n"