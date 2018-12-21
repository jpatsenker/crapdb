import subprocess
import os

PYTHON_PATH = '/usr/bin/python'

#p = subprocess.Popen(['whoami'])
p = subprocess.Popen(['/usr/bin/srun', '--partition=short', '--time=1', PYTHON_PATH, 'test_slurm.py'])
p.wait()
print "Done"

