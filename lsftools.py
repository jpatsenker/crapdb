import subprocess
def run_job(command, output="/dev/null", queue = "short", timelim = 1, wait = False, return_process = False, clean=False):
    a = subprocess.Popen(["/bin/bash", "-c" ,"./run_with_profile.sh -q " + queue + " -K -W " + str(timelim) + " -o " + output + " " + command])
    if wait:
        a.wait()
    if clean && output!="/dev/null":
        clean_file(output)
    if return_process:
        return a

def clean_file(file_name):
    with open(file_name, "r") as raw_file:
        everything = raw_file.read()
    split_stream = everything.split("------------------------------------------------------------" + "\n" + "Sender: LSF System")
    with open(file_name, "w") as out_here:
        out_here.write(split_stream[0])
