import subprocess

p = subprocess.Popen(['/bin/bash', '-c', './run_with_profile.sh -q short -W 1 -K -o superlog -e superlog "echo \'Hello World\' >> superlog"'])
p.wait()
print "Done"

