print "running..."
import sys
import os
"""
#Interface for running run_cra from php
"""

#os.chdir('/n/www/kirschner.med.harvard.edu/docroot/corecop')

#sys.path.append('/n/www/kirschner.med.harvard.edu/docroot/corecop')
#sys.path.append('/n/www/kirschner.med.harvard.edu/docroot/corecop/aux')


import subprocess


"""
Toolbox for working with LOGS
"""


CONTACT_EMAIL = "<contact-email>"

def add_line_to_log(log_file, line):
    with open(log_file, "a") as lfil:
        lfil.write(str(line) + "\n")


def srun(command, error, output, queue, timelim, wait):
    full_command = ['/usr/bin/sbatch', '-D'+str(os.getcwd()), '--partition='+str(queue),
                    '--time='+str(timelim), '--output='+str(output),
                    '--error='+str(error), "--wrap='%s'" % command ]
    full_command_str = " ".join(full_command)
    print full_command_str
    proc = subprocess.Popen(full_command)
    #temporarily disabled
#    if wait:
#        proc.wait()
    return proc



class Job:
    def __init__(self, job_string, lfil=None):
        self.job_string = job_string
        self.lfil = lfil

    def run(self, error = 'error_test', output='output_test', queue='short', timelim = 60, wait = False, return_process = False):
        if self.lfil is not None:
            logtools.add_line_to_log(self.lfil, "<CMD:> [SRUN] " + self.job_string)

        proc = srun(self.job_string, error, output, queue, timelim, wait)

        if wait and self.lfil is not None:
            logtools.add_line_to_log(self.lfil, "<CMD EXECUTED>")

        if return_process:
            return proc

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

job = Job(command_string)
job.run(wait=True, output="interface_test_out", error="interface_test_err")

print "done"
