import lsftools
import sys
import os

command_string = "python process_crap.py"

for a in sys.argv[1:]:
    command_string += " " + a

print command_string + "\n"
lsftools.run_job(command_string, wait=True, dont_clean=True, bsub_output=os.ttyname(sys.stdout.fileno()), bsub_error=os.ttyname(sys.stderr.fileno()))

print "done"