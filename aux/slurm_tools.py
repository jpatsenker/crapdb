import subprocess


def srun(command, error, output, queue, timelim, wait):
    full_command = ['/usr/bin/srun', '--partition='+str(queue), '--time='+str(timelim), '--output='+str(output), '--error='+str(error)]
    full_command.extend(command.split())
    full_command_str = full_command.join(' ')
    print full_command_str
    proc = subprocess.call(full_command_str)
    if wait:
        proc.wait()
    return proc