import subprocess

from aux import logtools

"""
Toolbox for running commands on lsf (with bsub)
"""

def run_job(command, bsub_output="/dev/null", bsub_error="/dev/null", queue = "short", timelim = 60, wait = False, return_process = False, dont_clean=False, lfil = None):

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
		logtools.add_line_to_log(lfil, "<CMD:> bsub -q " + queue + " -K -W " + str(timelim) + " -o " + bsub_output + " -e " + bsub_error + " " + command)
		#logtools.add_line_to_log(lfil, "bsub -q " + queue + " -K -W " + str(timelim) + " " + command)

	a = subprocess.Popen(["/bin/bash", "-c" ,"./aux/run_with_profile.sh -q " + queue + " -K -W " + str(timelim) + " -o " + bsub_output + " -e " + bsub_error + " " + command])
	if wait:
		a.wait()
		if lfil is not None:
			logtools.add_line_to_log(lfil, "<CMD EXECUTED>")
	if bsub_output!="/dev/null" and not dont_clean:
		clean_file(bsub_output)
	if return_process:
		return a


def run_job_set(commands, bsub_output="/dev/null", bsub_error="/dev/null", queue = "short", timelim = 60, wait = True, return_process = False, dont_clean=False, lfil = None):

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

	for command in commands:
		if lfil is not None:
			logtools.add_line_to_log(lfil, "bsub -q " + queue + " -K -W " + str(timelim) + " -o " + bsub_output + " -e " + bsub_error + " " + command)
		#logtools.add_line_to_log(lfil, "bsub -q " + queue + " -K -W " + str(timelim) + " " + command)

	a = []
	for i in range(len(commands)):
		print commands[i]
		a.append(subprocess.Popen(["/bin/bash", "-c" ,"./aux/run_with_profile.sh -q " + queue + " -K -W " + str(timelim) + " -o " + bsub_output + " -e " + bsub_error + " " + commands[i]]))
	for i in range(len(a)):
		a[i].wait()
	if bsub_output!="/dev/null" and not dont_clean:
		clean_file(bsub_output)
	if return_process:
		return a

def run_hmmer_parallel(inputFile, referenceFile, outputFile, bsub_output="/dev/null", bsub_error="/dev/null", lfil = None):
	"""
	Specifically for running hmmer in parallel. Very resource intensive
	TODO: MAY NEED RESOURCE CALCULATIONS, OR CHOOSING BETTER QUEUES
	:param inputFile:
	:param referenceFile:
	:param outputFile:
	:param bsub_output:
	:param bsub_error:
	:param lfil:
	:return:
	"""
	if lfil is not None:
		logtools.add_line_to_log(lfil, 'bsub -q parallel -K -W 16:00 -o test/testParallel.stdout -e test/testParallel.stderr -n 50 -R "rusage[mem=2000]span[ptile=8]" -o ' + bsub_output + ' -e ' + bsub_error + ' phmmer --domtblout ' + outputFile + " " + inputFile + " " + referenceFile)
	a = subprocess.Popen(["/bin/bash", "-c" ,'./aux/run_with_profile.sh -q parallel -K -W 16:00 -o test/testParallel.stdout -e test/testParallel.stderr -n 50 -R "rusage[mem=2000]span[ptile=8]" -o ' + bsub_output + ' -e ' + bsub_error + ' phmmer --domtblout ' + outputFile + " " + inputFile + " " + referenceFile])
	a.wait()
	if lfil is not None:
		logtools.add_line_to_log(lfil, "<HMMER COMPLETE>")
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