import lsftools
import sys
import os

command_string = "python process_crap.py"

for a in sys.argv[1:]:
    command_string += " " + a

print command_string + "\n"
lsftools.run_job(command_string, wait=True, dont_clean=True, bsub_output="tmp/tmp_superlog", bsub_error="tmp/tmp_superlog_err")

print "done"