import lsftools
import sys

command_string = "python process_crap.py"

for a in sys.argv[1:]:
    command_string += " " + a

print command_string + "\n"
lsftools.run_job(command_string, wait=True)

print "done"