from sequence_length_filter import SeqLengthFilter
from sewagesystem import SewageSystem
import mailtools
import sys
import os


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

ss = SewageSystem()

len_filter = SeqLengthFilter(30, 30000)

ss.add_filter(len_filter)

ss.filter_crap(iFile, oFile, dFile, tDir)

mailtools.send_email("Nothing yet", eAddress, [oFile, dFile])