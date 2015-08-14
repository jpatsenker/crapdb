from sequence_length_filter import SeqLengthFilter
from num_seq_analyzer import NumSeqAnalyzer
from sewagesystem import SewageSystem
import mailtools
import sys
import os
import fasta_fixer
import logtools


iFile = None
oFile = None
dFile = None
tDir = "tmp/"
eAddress = None

try:
    iFile = sys.argv[1]
    oFile = sys.argv[2]
    dFile = sys.argv[3]
    eAddress = sys.argv[4]
except IndexError:
    print "Too Few Arguments for process_crap.py \n"
    exit(1)

if "@" not in eAddress:
    print "Invalid email given to process_crap.py \n"
    exit(1)

if not os.path.isdir(tDir):
    print "Invalid temporary directory\n"
    exit(1)

if not os.path.exists(iFile):
    print "Invalid input fasta\n"
    exit(1)

logfil = "logs/" + os.path.basename(iFile) + ".log"

try:
    os.remove(logfil)
except OSError:
    pass

try:
    os.remove(oFile)
except OSError:
    pass


try:
    os.remove(dFile)
except OSError:
    pass

logtools.start_new_log(iFile, eAddress, logfil)

fasta_fixer.fix_file(iFile)

ss = SewageSystem()

num_seq_bef_anlzr = NumSeqAnalyzer()
num_seq_aft_anlzr = NumSeqAnalyzer()
len_filter = SeqLengthFilter(30, 30000)

ss.add_module(num_seq_bef_anlzr)
ss.add_module(len_filter)
ss.add_module(num_seq_aft_anlzr)

aFiles = ss.flush_the_toilet(iFile, oFile, dFile, tDir, log=logfil)

assert len(aFiles) == 2
with open(aFiles[0], "r") as analysisFile:
    before_seq = analysisFile.read()
with open(aFiles[1], "r") as analysisFile:
    after_seq = analysisFile.read()

crap_score = 1 - float(after_seq)/float(before_seq)

mailtools.send_email("Final Crap Score: " + str(crap_score) + '\n See clean and messy files below, and log here: <a href="' +  os.path.abspath(logfil) + '"> log </a> <br>', eAddress, [oFile, dFile])