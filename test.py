import subprocess
import os

p = subprocess.Popen(['srun -p short -t 1 -o stdout.txt -e stderr.txt python slurm_test.py'], preexec_fn=lambda: os.system("sudo -s -u kirschner"))
p.wait()
print "Done"

