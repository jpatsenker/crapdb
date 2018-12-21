import subprocess
import os

p = subprocess.Popen(['srun -p short -t 1 -o stdout.txt -e stderr.txt echo \'Hello World\''])
p.wait()
print "Done"

