print "running..."
import sys
import os
import aux.jobs
"""
#Interface for running run_cra from php
"""

"""
Toolbox for working with LOGS
"""

CONTACT_EMAIL = "<contact-email>"

def add_line_to_log(log_file, line):
    with open(log_file, "a") as lfil:
        lfil.write(str(line) + "\n")

if __name__ == '__main__':
    sys.stdout.write('%s\n' % os.getcwd())
    sys.stdout.flush()
    sys.stderr.flush()
    command_string = "python run_cra.py %s" % ' '.join(sys.argv[1:])
    sys.stdout.write(command_string + "\n\n")
    job = aux.jobs.Job(command_string)
    job.run(wait=False, output="interface_test_out", error="interface_test_err")
    sys.stdout.write("done\n")
