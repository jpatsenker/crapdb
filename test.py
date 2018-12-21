import subprocess
import os

#p = subprocess.Popen(['whoami'])
p = subprocess.call('srun -p short -t 1 "python test_slurm.py"')
p.wait()
print "Done"

