from sequence_length_filter import SeqLengthFilter
from num_seq_analyzer import NumSeqAnalyzer
from sewagesystem import SewageSystem
from zeroj_filter import ComplexityFilter
from cdhit_filter import RedundancyFilter
from simple_crap_filter import SimpleFilter
from fasta_filter import FastaCheckerFilter
from fusfis_filter import FusionFissionFilter
import lsftools
import mailtools
import sys
import os
import zipfile
import fasta_fixer
import logtools


iZip = None
oFile = None
tDir = "tmp/"
eAddress = None

try:
    iZip = sys.argv[1]
    oFile = sys.argv[2]
    eAddress = sys.argv[3]
except IndexError:
    print "Too Few Arguments for process_crap_batch.py \n"
    exit(1)

if "@" not in eAddress:
    print "Invalid email given to process_crap_batch.py \n"
    exit(1)

if not os.path.isdir(tDir):
    print "Invalid temporary directory\n"
    exit(1)

if not os.path.exists(iZip):
    print "Invalid input fasta\n"
    exit(1)

logfil = "logs/" + os.path.basename(iZip) + ".log"

try:
    os.remove(logfil)
except OSError:
    pass

try:
    os.remove(oFile)
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



if len(sys.argv) > 4:
    if "-0j" in sys.argv[4:]:
        zeroj_param = float(sys.argv[sys.argv.index("-0j")+1])
    if "-ct" in sys.argv[4:]:
        cdhit_param_thresh = float(sys.argv[sys.argv.index("-ct")+1])
    if "-cl" in sys.argv[4:]:
        cdhit_param_flength = float(sys.argv[sys.argv.index("-cl")+1])
    if "-min" in sys.argv[4:]:
        min_len_param = int(sys.argv[sys.argv.index("-min")+1])
    if "-max" in sys.argv[4:]:
        max_len_param = int(sys.argv[sys.argv.index("-max")+1])
    if "-fft" in sys.argv[4:]:
        ff_param_thresh = float(sys.argv[sys.argv.index("-fft")+1])
    if "-ffl" in sys.argv[4:]:
        ff_param_flength = float(sys.argv[sys.argv.index("-ffl")+1])
    if "-ms" in sys.argv[4:]:
        ms_check = True
    if "-xs" in sys.argv[4:]:
        xs_tolerance = int(sys.argv[sys.argv.index("-xs")+1])
    # if "-nofasta" in sys.argv[5:]: #not recommended
    #     no_fasta = True
    # if "-nosimple" in sys.argv[5:]: #not recommended
    #     no_simple = True
    if "-nolen" in sys.argv[4:]:
        no_len = True
    if "-nocomp" in sys.argv[4:]:
        no_comp = True
    if "-nored" in sys.argv[4:]:
        no_red = True
    if "-noff" in sys.argv[4:]:
        no_fusfis = True



zip_ref = zipfile.ZipFile(iZip, 'r')
iFilesDir = iZip.split(".zip")[0]
zip_ref.extractall(os.path.basename(iZip))
iFiles = os.listdir(iFilesDir)
for x in range(len(iFiles)):
    iFile = iFiles[x]
    iFiles[x] = iFilesDir + "/" + iFile

print iFiles
exit(0)
params = iFiles[0] + " /dev/null /dev/null " + oFile + " " + eAddress + " 1"
for a in sys.argv[4:]:
    params += " " + a
lsftools.run_job("python process_crap.py " + params, wait=True, dont_clean=True, bsub_output="/dev/null", bsub_error="/dev/null")


for iFile in iFiles[1:]:
    params = iFile + " /dev/null /dev/null " + oFile + " " + eAddress + " 0"
    for a in sys.argv[4:]:
        params += " " + a
    lsftools.run_job("python process_crap.py " + params, wait=True, dont_clean=True, bsub_output="/dev/null", bsub_error="/dev/null")



para_str = ""
for a in sys.argv[1:]:
    if a[0] == "-":
        para_str += "<br>" + a
    else:
        para_str += " " + a

mailtools.send_email("We ran CRAP version 2.0 [BATCH] on files in " + iZip + "<br>Here is a list of parameters used: <br>" + para_str + '<br>', eAddress, [oFile])


#os.rmtree(iFilesDir)
