import subprocess
def run_job(command, output="/dev/null", queue = "short", timelim = 1, wait = False, return_process = False):
    a = subprocess.Popen(["/bin/bash", "-c" ,"./run_with_profile.sh -q " + queue + " -W " + str(timelim) + " -o " + output + " " + command])
    if wait:
        a.wait()
    if return_process:
        return a