import subprocess
import sys
import shlex


def process_run(cmd_string, stdin=None):
    """Given a string representing a single command, open a process, and return
    the Popen process object.
    >>> process_object = process_run('echo test')
    >>> isinstance(process_object, subprocess.Popen)
    True
    """
    return subprocess.Popen(shlex.split(cmd_string),
                            stdin=stdin,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)


def process_results(process_object):
    """Given a process object, wait for it to complete then return a tuple:
    >>> (returncode, stdout, stderr) = process_results(process_run('echo my process'))
    >>> returncode
    0
    >>> stdout
    'my process\\n'
    >>> stderr
    ''
    """
    (stdout, stderr)=process_object.communicate()
    return (process_object.returncode, stdout, stderr)


def process(cmd_string, stdin=None):
    """Given a string representing a single command, open a process, wait for it to terminate and then
    return standard out and standard in as a tuple

    >>> process("echo 1 2")
    (0, '1 2\\n', '')
    """
    return process_results(process_run(cmd_string, stdin=stdin))
