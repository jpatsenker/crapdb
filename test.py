import subprocess
import os

p = subprocess.Popen(['sudo -u kirschner "srun -p short -t 1 python slurm_test.py"'])
p.wait()
print "Done"

