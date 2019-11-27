print "running..."
import sys
import os
import aux.jobs
"""
#Interface for running run_cra from php
"""

#os.chdir('/n/www/kirschner.med.harvard.edu/docroot/corecop')

#sys.path.append('/n/www/kirschner.med.harvard.edu/docroot/corecop')
#sys.path.append('/n/www/kirschner.med.harvard.edu/docroot/corecop/aux')


#import subprocess


"""
Toolbox for working with LOGS
"""


CONTACT_EMAIL = "<contact-email>"

def add_line_to_log(log_file, line):
    with open(log_file, "a") as lfil:
        lfil.write(str(line) + "\n")

#print os.getcwd()
#import aux
#import aux.jobs
#import jobs
sys.stdout.flush()
sys.stderr.flush()
command_string = "python run_cra.py"

for a in sys.argv[1:]:
    command_string += " " + a

print command_string + "\n"

job = aux.jobs.Job(command_string)
job.run(wait=False, output="interface_test_out", error="interface_test_err")

print "done"
