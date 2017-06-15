import subprocess
import random

def runBlast(sequences, reference, output):
	"""
	Run Blast on the sequences fasta file, with a reference fasta file, write to output
	:param sequences:
	:param reference:
	:param output:
	:return:
	"""
	loadBlast()
	name = random.random()
	out = random.random()
	makedb = subprocess.Popen("makeblastdb -in " + reference + " -dbtype 'prot' -out " + out + " -name " + name)
	makedb.wait()
	run = subprocess.Popen("blastp -outfmt 8 -evalue 1e-5 -db " + name + " -query " + sequences + " -out " + output)
	run.wait()

def loadBlast():
	"""
	Load Blast
	:return:
	"""
	p = subprocess.Popen("module load seq")
	p.wait()