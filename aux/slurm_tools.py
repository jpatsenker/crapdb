import subprocess


def srun(command, error, output, queue, timelim, wait):
    full_command = ['/usr/bin/srun', '--partition='+str(queue), '--time='+str(timelim), '--output='+str(output), '--error='+str(error)]
    full_command.extend(command.split())
    full_command_str = " ".join(full_command)
    print full_command_str
    proc = subprocess.Popen(full_command)
    if wait:
        proc.wait()
    return proc