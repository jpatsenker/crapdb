import subprocess


def srun(command, error, output, queue, timelim, wait):
    full_command = ['/usr/bin/srun', '--partition=short', '--time=1', command]
    print full_command
    proc = subprocess.Popen(full_command)
    if wait:
        proc.wait()
    return proc