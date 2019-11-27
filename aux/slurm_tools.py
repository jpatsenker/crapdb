import sys
import subprocess
from proctools import process
from datetime import datetime

def srun(command, error, output, queue, timelim, wait):
    full_command = ['/usr/bin/srun', '--partition='+str(queue), '--time='+str(timelim), '--output='+str(output), '--error='+str(error)]
    full_command.extend(command.split())
    full_command_str = " ".join(full_command)
    print full_command_str
    proc = subprocess.Popen(full_command)
    if wait:
        proc.wait()
    return proc

def sbatch_params(command, **params):
    param_list=[]
    for param in params:
        if len(param) == 1:
            if isinstance(params[param], bool):
                if params[param]:
                    param_list.append('-%s' % param)
            else:
                param_list.append('-%s %s' % (param, params[param]))
        else:
            if isinstance(params[param], bool):
                if params[param]:
                    param_list.append('--%s' % param)
            else:
                param_list.append('--%s=%s' % (param, params[param]))
    param_list.append("--wrap='%s'" % command)
    return ' '.join(param_list)

def sbatch(command, error, output, queue, timelim, wait):
    timestamp=datetime.today().strftime("%Y%m%d-%H%M%S-%f")
    params=sbatch_params(command,
                         error=error,
                         output=output, partition=queue, time=timelim, wait=wait)
    cmdlogout="log/cmdlogfile.%s.out" % timestamp
    cmdlogerr="log/cmdlogfile.%s.err" % timestamp
    full_command='sbatch %s' % params
    cmdout=open(cmdlogout, 'w')
    cmderr=open(cmdlogerr, 'w')
    cmdout.write("%s\n" % full_command)
    rc, op, er = process(full_command)
    cmdout.write(op)
    cmderr.write(er)
    cmdout.close()
    cmderr.close()
    return rc
