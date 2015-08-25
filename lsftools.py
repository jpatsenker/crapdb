import subprocess
import logtools
def run_job(command, bsub_output="/dev/null", bsub_error="/dev/null", queue = "long", timelim = 60, wait = False, return_process = False, dont_clean=False, lfil = None):

    """
    :param command: Command to be submitted to LSF
    :param bsub_output: Where output should be routed to (default: /dev/null)
    :param queue: What queue the command should be submitted to (default: short)
    :param timelim: How much time is allowed for command to run (default: 1)
    :param wait: Whether or not to wait for command to execute (default: False)
    :param return_process: Whether or not to return subprocess object (default: False)
    :param dont_clean: Whether or not to clean output in case its not /dev/null (default: False)
    :return: subprocess object in case return_process=True.
    """

    if lfil is not None:
        logtools.add_line_to_log(lfil, "bsub -q " + queue + " -K -W " + str(timelim) + " -o " + bsub_output + " -e " + bsub_error + " " + command)

    a = subprocess.Popen(["/bin/bash", "-c" ,"./run_with_profile.sh -q " + queue + " -K -W " + str(timelim) + " -o " + bsub_output + " -e " + bsub_error + " " + command])
    if wait:
        a.wait()
    if bsub_output!="/dev/null" and not dont_clean:
        clean_file(bsub_output)
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
    open(file_name, "w").close()
    with open(file_name, "w") as out_here:
        out_here.write(split_stream[0].rstrip("\n"))