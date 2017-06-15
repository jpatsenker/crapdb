import sys

from aux import lsftools
"""
Interface for running run_cra from php
"""


command_string = "python run_cra.py"

for a in sys.argv[1:]:
    command_string += " " + a

print command_string + "\n"
lsftools.run_job(command_string, wait=True, dont_clean=True, bsub_output="/dev/null", bsub_error="/dev/null")

print "done"