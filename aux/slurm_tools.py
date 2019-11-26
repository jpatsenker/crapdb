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


def sbatch(command, error, output, queue, timelim, wait):
    full_command=['/bin/sbatch', '--partition='+str(queue), '--time='+str(timelim), '--output='+str(output), '--error='+str(error)]
    if wait:
        full_command.append('--wait')
    full_command.append("--wrap='%s'" % command)
    print ' '.join(full_command)
    proc=subprocess.Popen(full_command)
    if wait:
        proc.wait()
    return proc
