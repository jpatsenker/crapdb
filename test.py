import subprocess
import os

p = subprocess.Popen(['sudo -s -u kirschner srun -p short -t 1 python test_slurm.py'])
#p = subprocess.Popen(['srun -p short -t 1 -uid=kirschner python test_slurm.py'])
p.wait()
print "Done"

