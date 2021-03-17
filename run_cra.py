import sys
import os

from filters.sequence_length_filter import SeqLengthFilter
from analyzers.num_seq_analyzer import NumSeqAnalyzer
from sewagesystem import SewageSystem
from filters.sewagefilter import BrokenFilterError
from filters.complexity_filter import ComplexityFilter
from filters.redundancy_filter import RedundancyFilter
from filters.simple_filter import SimpleFilter
from filters.fasta_filter import FastaCheckerFilter
#from filters.fission_filter import FissionFilter
from aux import logtools, mailtools, fasta_fixer, helptools

#DEFAULT REFERENCE FILES FOR CONCAT FILTER
#HUMAN_GENOME_FILE = "data/reference_genomes/hgfix.fa"
#XTROP_GENOME_FILE = "data/reference_genomes/xtfix.fa"


#params init
iFile = None
oFile = None
dFile = None
tDir = os.getenv('CRA_SCRATCH', default="/n/groups/kirschner_www/corecop/")

eAddress = None

#pull params from command line
try:
    iFile = sys.argv[1]
    iFile_new = iFile + "fix"
    oFile = sys.argv[2]
    dFile = sys.argv[3]
    eAddress = sys.argv[4]
except IndexError:
    helptools.printHelp()
    exit(1)


if not os.path.exists(iFile):
    print "Invalid input fasta\n"
    exit(1)

#create the log file
logfil = os.path.join("logs/", os.path.basename(iFile) + ".log")

#make sure email is somewhat valid
if "@" not in eAddress:
    print "Invalid email given to run_cra.py \n"
    logtools.add_fatal_error(logfil, "Invalid email address")
    exit(1)

#make sure the the tmp directory exists
if not os.path.isdir(tDir):
    print "Invalid temporary directory\n"
    logtools.add_fatal_error(logfil, "Invalid temporary directory set. FURTHER SERVER SETUP REQUIRED")
    mailtools.send_error("Invalid temporary directory set. FURTHER SERVER SETUP REQUIRED", eAddress)
    exit(1)


#if log file exists, remove it
try:
    os.remove(logfil)
except OSError:
    pass

#if output file exists, remove it
try:
    os.remove(oFile)
except OSError:
    pass

#if diagnosis file exists, remove it
try:
    os.remove(dFile)
except OSError:
    pass


#Default Parameters
zeroj_param = .9
cdhit_param_thresh = .7
cdhit_param_flength = .8
min_len_param = 30
max_len_param = 30000
ff_param_thresh = .7
ff_param_flength = .8
ms_check = False
xs_tolerance = 0
#refGenome = "human"

#ignore filters params
no_len = False
no_comp = False
no_red = False
no_fis = False
no_fus = False

#pull parameters from command line
try:
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
        if "-fft" in sys.argv[5:]:
            ff_param_thresh = float(sys.argv[sys.argv.index("-fft")+1])
        if "-ffl" in sys.argv[5:]:
            ff_param_flength = float(sys.argv[sys.argv.index("-ffl")+1])
        if "-ms" in sys.argv[5:]:
            ms_check = True
        if "-xs" in sys.argv[5:]:
            xs_tolerance = int(sys.argv[sys.argv.index("-xs")+1])
        #if "-rg" in sys.argv[5:]:
        #    refGenome = sys.argv[sys.argv.index("-rg")+1]
        if "-nolen" in sys.argv[5:]:
            no_len = True
        if "-nocomp" in sys.argv[5:]:
            no_comp = True
        if "-nored" in sys.argv[5:]:
            no_red = True
        if "-nofis" in sys.argv[5:]:
            no_fis = True
        if "-nofus" in sys.argv[5:]:
            no_fus = True
except ValueError:
    helptools.printHelp()
    exit(1)

#reference genome set
#if refGenome == "human": #default
#    refGenome = HUMAN_GENOME_FILE
#if refGenome == "xtrop": #default
#    refGenome = XTROP_GENOME_FILE
#else:
#    if not os.path.exists(refGenome): #use file
#        logtools.add_fatal_error(logfil, "Invalid Reference Genome File: " + refGenome)
#        mailtools.send_error("Invalid Reference Genome File: " + refGenome, eAddress, lfil=logfil)
#        print "Invalid Reference Genome File: " + refGenome + "\n"
#        exit(1)

#start log file
logtools.start_new_log(iFile, eAddress, logfil)

#run fasta fixer
fasta_fixer.fix_file(iFile, iFile_new)
iFile = iFile_new
"""^THIS IS STILL NECESSARY AS NOT ALL FILTERS/ANALYZERS USE FastaReader/FastaWriter"""

#initialize system object
ss = SewageSystem()

#initialize all filters/analyzers
num_seq_bef_anlzr = NumSeqAnalyzer(logfil, dFile)
num_seq_aft_anlzr = NumSeqAnalyzer(logfil, dFile)
len_filter = SeqLengthFilter(min_len_param, max_len_param)
comp_filter = ComplexityFilter(zeroj_param, tDir, lfil=logfil)
red_filter = RedundancyFilter(cdhit_param_thresh, cdhit_param_flength, tDir, lfil=logfil)
simple_filter = SimpleFilter(ms_check, xs_tolerance)
fasta_filter = FastaCheckerFilter(tDir)
#fission_filter = FissionFilter(refGenome, tDir)

#queue all modules in order
ss.add_module(num_seq_bef_anlzr) #check before

#for debugging/log files, create a few more analyzers
a = []
for i in range(5):
    a.append(NumSeqAnalyzer(logfil, dFile))


logtools.add_to_log("STAGING ALL FILTERS", logfil)
logtools.add_start(logfil)

#FILTERS
ss.add_module(fasta_filter)
logtools.add_line_to_log(logfil, "<Staging Fasta Filter>")
ss.add_module(a[0])
ss.add_module(simple_filter)
logtools.add_line_to_log(logfil, "<Staging Simple Filter>")
if not no_len:
    ss.add_module(a[1])
    ss.add_module(len_filter)
    logtools.add_line_to_log(logfil, "<Staging Length Filter>")
    print "Staging Length Filter"
if not no_comp:
    ss.add_module(a[2])
    ss.add_module(comp_filter)
    logtools.add_line_to_log(logfil, "<Staging Complexity Filter>")
    print "Staging Complexity Filter"
if not no_red:
    ss.add_module(a[3])
    ss.add_module(red_filter)
    logtools.add_line_to_log(logfil, "<Staging Redundancy Filter>")
    print "Staging Redundancy Filter"

# if not no_fis:
#     ss.add_module(a[4])
#     ss.add_module(fission_filter)
#     logtools.add_line_to_log(logfil, "<Staging Fission Filter>")
#     print "Staging Fission Filter"

ss.add_module(num_seq_aft_anlzr) #check after

logtools.add_end(logfil)

open(dFile, "w").close()

#run the system
try:
    aFiles = ss.flush_the_toilet(iFile, oFile, dFile, tDir, log=logfil)
except BrokenFilterError:
    print "A Filter has broken!"
    logtools.add_fatal_error(logfil, "\n<><><><><><><><><><><><><><><><><><>\nFATAL ERROR CAUGHT SENDING EMAIL\n<><><><><><><><><><><><><><><><><><>\n!!!!!!!")
    mailtools.send_error('An internal error occured running your job, please check the log for more information:<br> Log: <a href="' + os.getcwd().replace("/docroot","").split("/www/")[1] + '/' + logfil + '"> Log File </a><br>', eAddress, lfil=logfil)
    exit(1)
except Exception as e:
    print "An unknown error has occurred!!!"
    logtools.add_fatal_error(logfil, "\n<><><><><><><><><><><><><><><><><><>\nFATAL ERROR CAUGHT SENDING EMAIL\n<><><><><><><><><><><><><><><><><><>\n!!!!!!!")
    mailtools.send_error('An internal error occured running your job, please check the log for more information:<br> Log: <a href="' + os.getcwd().replace("/docroot","").split("/www/")[1] + '/' + logfil + '"> Log File </a><br>', eAddress, lfil=logfil)
    raise e, None, sys.exc_info()[2]

#Prepare output
with open(aFiles[0], "r") as analysisFile:
    before_seq = analysisFile.read()
with open(aFiles[-1], "r") as analysisFile:
    after_seq = analysisFile.read()

#score
cra_score = 1 - float(after_seq)/float(before_seq)

fullpath = os.getcwd()[os.getcwd().find("/www/") + 5:] +  "/" +  logfil

fullpath = fullpath.replace("/docroot/", '/')

para_str = ""
for a in sys.argv[1:]:
    if a[0] == "-":
        para_str += "<br>" + a
    else:
        para_str += " " + a

inputFileName = iFile[iFile.rfind('/')+1:iFile.rfind('fix')]

#send email
mailtools.send_email("We ran CoReCop version 1.1 on file " + inputFileName + "<br>Here is a list of parameters used: <br>" + para_str + "<p>Initial Number of Sequences: " + str(before_seq) + "<br>Number of Clean Sequences: " + str(after_seq) + "<br>Final CoReCop Score: " + ("%.3f" % cra_score) + '<br> See clean and messy files below, and log here: https://' + fullpath + '<br>', eAddress, [oFile, dFile], lfil=logfil, sub="CoReCop run on " + inputFileName)
#log
logtools.end_log(logfil)
