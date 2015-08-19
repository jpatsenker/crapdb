from sequence_length_filter import SeqLengthFilter
from num_seq_analyzer import NumSeqAnalyzer
from sewagesystem import SewageSystem
from zeroj_filter import ComplexityFilter
from cdhit_filter import RedundancyFilter
from simple_crap_filter import SimpleFilter
from fasta_filter import FastaCheckerFilter
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


zeroj_param = .9
cdhit_param_thresh = .7
cdhit_param_flength = .8
min_len_param = 30
max_len_param = 30000
completeness_analysis = True

if len(sys.argv) > 5:
    if "-0j" in sys.argv[5:]:
        zeroj_param = float(sys.argv[sys.argv.index("-0j")+1])
    if "-ct" in sys.argv[5:]:
        cdhit_param_thresh = float(sys.argv[sys.argv.index("-ct")+1])
    if "-cl" in sys.argv[5:]:
        cdhit_param_flength = float(sys.argv[sys.argv.index("-cl")+1])
    if "-min" in sys.argv[5:]:
        min_len_param = int(sys.argv[sys.argv.index("-min")+1])
    if "-max" in sys.argv[5:]:
        max_len_param = int(sys.argv[sys.argv.index("-max")+1])
    if "-nocomp" in sys.argv[5:]:
        completeness_analysis = False


logtools.start_new_log(iFile, eAddress, logfil)

#fasta_fixer.fix_file(iFile)

ss = SewageSystem()

num_seq_bef_anlzr = NumSeqAnalyzer()
num_seq_aft_anlzr = NumSeqAnalyzer()
len_filter = SeqLengthFilter(min_len_param, max_len_param)
comp_filter = ComplexityFilter(zeroj_param)
red_filter = RedundancyFilter(cdhit_param_thresh, cdhit_param_flength)
simple_filter = SimpleFilter()
fasta_filter = FastaCheckerFilter()

ss.add_module(num_seq_bef_anlzr) #check before


#FILTERS
#ss.add_module(len_filter)
#ss.add_module(comp_filter)
#ss.add_module(red_filter)
#ss.add_module(simple_filter)
ss.add_module(fasta_filter)

ss.add_module(num_seq_aft_anlzr) #check after

aFiles = ss.flush_the_toilet(iFile, oFile, dFile, tDir, log=logfil)

assert len(aFiles) == 2
with open(aFiles[0], "r") as analysisFile:
    before_seq = analysisFile.read()
with open(aFiles[1], "r") as analysisFile:
    after_seq = analysisFile.read()

crap_score = 1 - float(after_seq)/float(before_seq)

fullpath = os.getcwd()[os.getcwd().find("/www/") + 5:] +  "/" +  logfil

fullpath = fullpath.replace("/docroot/", '/')

mailtools.send_email("Final Crap Score: " + str(crap_score) + '\n See clean and messy files below, and log here: ' + fullpath + '<br>', eAddress, [oFile, dFile])