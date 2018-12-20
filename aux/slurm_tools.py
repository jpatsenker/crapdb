import subprocess


def srun(command, error, output, queue, timelim, wait):
    full_command = "srun -p " + queue + " -t " + str(timelim) + " -o " + output + " -e " + error + " " + command
    print full_command
    proc = subprocess.Popen([full_command])
    if wait:
        proc.wait()
    return proc