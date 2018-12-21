import subprocess
import os

p = subprocess.Popen(['srun -p short -t 1 -o stdout.txt -e stderr.txt echo \'Hello World\''], preexec_fn=lambda: os.system("sudo -i -u kirshner"))
p.wait()
print "Done"

