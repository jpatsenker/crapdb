import subprocess



p = subprocess.Popen('./run_with_profile.sh echo hi')
p.wait()
