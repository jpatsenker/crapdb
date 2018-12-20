import subprocess


def srun(job_string, error, output, queue, timelim, wait):
    full_command = "slurm -p " + queue + " -t " + str(timelim) + " -o " + output + " -e " + error + " " + command
    print full_command
    proc = 'lol'
    #proc = subprocess.Popen([full_command])
    if wait:
        proc.wait()
    return proc