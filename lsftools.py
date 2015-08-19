import subprocess
def run_job(command, output="/dev/null", queue = "short", timelim = 1, wait = False, return_process = False, dont_clean=False):
    """
    :param command: Command to be submitted to LSF
    :param output: Where output should be routed to (default: /dev/null)
    :param queue: What queue the command should be submitted to (default: short)
    :param timelim: How much time is allowed for command to run (default: 1)
    :param wait: Whether or not to wait for command to execute (default: False)
    :param return_process: Whether or not to return subprocess object (default: False)
    :param dont_clean: Whether or not to clean output in case its not /dev/null (default: False)
    :return: subprocess object in case return_process=True.
    """
    print ["/bin/bash", "-c" ,"./run_with_profile.sh -q " + queue + " -K -W " + str(timelim) + " -o " + output + " " + command]
    a = subprocess.Popen(["/bin/bash", "-c" ,"./run_with_profile.sh -q " + queue + " -K -W " + str(timelim) + " -o " + output + " " + command])
    if wait:
        a.wait()
    if output!="/dev/null" and not dont_clean:
        print "cleaning " + output
        clean_file(output)
    if return_process:
        return a

def clean_file(file_name):
    """
    :param file_name: name of file to be cleaned of LSF trace signature
    :return:
    """
    with open(file_name, "r") as raw_file:
        everything = raw_file.read()
    split_stream = everything.split("------------------------------------------------------------" + "\n" + "Sender: LSF System")
    print '\n'
    print everything
    print '\n'
    open(file_name, "w").close()
    with open(file_name, "w") as out_here:
        out_here.write(split_stream[0].rstrip("\n"))
    exit(1)