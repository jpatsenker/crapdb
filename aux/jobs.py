from aux.slurm_tools import srun
from aux import logtools


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