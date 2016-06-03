import subprocess

def runHmmer(sequences, reference, output):
	loadBlast()
	run = subprocess.Popen("phmmer --tblout " + output + " " + name + " " + sequences)
	run.wait()

def loadHmmer():
	p = subprocess.Popen(". LOADHMMER.sh")
	p.wait()