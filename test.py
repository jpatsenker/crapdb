import subprocess
import os

p = subprocess.Popen(['srun -p short -t 1 "echo \'Hello World\'"'])
p.wait()
print "Done"

