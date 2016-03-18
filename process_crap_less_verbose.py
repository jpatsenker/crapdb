from sequence_length_filter import SeqLengthFilter
from num_seq_analyzer import NumSeqAnalyzer
from sewagesystem import SewageSystem
from zeroj_filter import ComplexityFilter
from cdhit_filter import RedundancyFilter
from simple_crap_filter import SimpleFilter
from fasta_filter import FastaCheckerFilter
from fusfis_filter import FusionFissionFilter
import mailtools
import sys
import os
import fasta_fixer
import logtools


iFile = None
oFile = None
dFile = None
finFile = None
tDir = "tmp/"
eAddress = None
isFirst=None

try:
    iFile = sys.argv[1]
    iFile_new = iFile + "fix"
    oFile = sys.argv[2]
    dFile = sys.argv[3]
    finFile = sys.argv[4]
    eAddress = sys.argv[5]
    isFirst = sys.argv[6]
except IndexError:
    print "Too Few Arguments for process_crap_less_verbose.py \n"
    exit(1)

if "@" not in eAddress:
    print "Invalid email given to process_crap_less_verbose.py \n"
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
ff_param_thresh = .7
ff_param_flength = .8
ms_check = False
xs_tolerance = 0

no_fasta = False
no_simple = False
no_len = False
no_comp = False
no_red = False
no_fusfis = False



if len(sys.argv) > 7:
    if "-0j" in sys.argv[7:]:
        zeroj_param = float(sys.argv[sys.argv.index("-0j")+1])
    if "-ct" in sys.argv[7:]:
        cdhit_param_thresh = float(sys.argv[sys.argv.index("-ct")+1])
    if "-cl" in sys.argv[7:]:
        cdhit_param_flength = float(sys.argv[sys.argv.index("-cl")+1])
    if "-min" in sys.argv[7:]:
        min_len_param = int(sys.argv[sys.argv.index("-min")+1])
    if "-max" in sys.argv[7:]:
        max_len_param = int(sys.argv[sys.argv.index("-max")+1])
    if "-fft" in sys.argv[7:]:
        ff_param_thresh = float(sys.argv[sys.argv.index("-fft")+1])
    if "-ffl" in sys.argv[7:]:
        ff_param_flength = float(sys.argv[sys.argv.index("-ffl")+1])
    if "-ms" in sys.argv[7:]:
        ms_check = True
    if "-xs" in sys.argv[7:]:
        xs_tolerance = int(sys.argv[sys.argv.index("-xs")+1])
    # if "-nofasta" in sys.argv[5:]: #not recommended
    #     no_fasta = True
    # if "-nosimple" in sys.argv[5:]: #not recommended
    #     no_simple = True
    if "-nolen" in sys.argv[7:]:
        no_len = True
    if "-nocomp" in sys.argv[7:]:
        no_comp = True
    if "-nored" in sys.argv[7:]:
        no_red = True
    if "-noff" in sys.argv[7:]:
        no_fusfis = True

logtools.start_new_log(iFile, eAddress, logfil)

fasta_fixer.fix_file(iFile, iFile_new)
iFile = iFile_new

ss = SewageSystem()

num_seq_bef_anlzr = NumSeqAnalyzer(logfil, dFile)
num_seq_aft_anlzr = NumSeqAnalyzer(logfil, dFile)
len_filter = SeqLengthFilter(min_len_param, max_len_param)
comp_filter = ComplexityFilter(zeroj_param, lfil=logfil)
red_filter = RedundancyFilter(cdhit_param_thresh, cdhit_param_flength, lfil=logfil)
simple_filter = SimpleFilter(ms_check, xs_tolerance)
fasta_filter = FastaCheckerFilter()
fusfis_filter = FusionFissionFilter(ff_param_thresh, ff_param_flength, lfil=logfil)

ss.add_module(num_seq_bef_anlzr) #check before

#for debugging
a = []
for i in range(5):
    a.append(NumSeqAnalyzer(logfil, dFile))

if isFirst:
    open(finFile, "w").close()

finCSVWriter = open(finFile, "a")


#FILTERS
if isFirst:
    finCSVWriter.write("Original")
ss.add_module(fasta_filter)
ss.add_module(a[0])
if isFirst:
    finCSVWriter.write(",Fasta")
ss.add_module(simple_filter)
if not no_len:
    ss.add_module(a[1])
    if isFirst:
        finCSVWriter.write(",Length")
    ss.add_module(len_filter)
if not no_comp:
    ss.add_module(a[2])
    if isFirst:
        finCSVWriter.write(",Complexity")
    ss.add_module(comp_filter)
if not no_red:
    ss.add_module(a[3])
    if isFirst:
        finCSVWriter.write(",Redundancy")
    ss.add_module(red_filter)
if not no_fusfis:
    ss.add_module(a[4])
    if isFirst:
        finCSVWriter.write(",Ff")
    ss.add_module(fusfis_filter)

finCSVWriter.write(",CrapScore\n")

ss.add_module(num_seq_aft_anlzr) #check after

open(dFile, "w").close()

aFiles = ss.flush_the_toilet(iFile, oFile, dFile, tDir, log=logfil)





with open(aFiles[0], "r") as analysisFile:
    before_seq = analysisFile.read()
with open(aFiles[-1], "r") as analysisFile:
    after_seq = analysisFile.read()

crap_score = 1 - float(after_seq)/float(before_seq)

crap_score_str = "%1.5f" % crap_score

print aFiles

for ind in range(len(aFiles)):
    with open(aFiles[ind], "r") as analysisFile:
        finCSVWriter.write(analysisFile.read())
        if ind < len(aFiles)-1:
            finCSVWriter.write(",")
        else:
            finCSVWriter.write("," + crap_score_str + "\n")



