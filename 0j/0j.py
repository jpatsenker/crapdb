#!/usr/bin/env python

# #!/sw/arch/bin/python

"""
This program takes sequences and finds low complexity regions by forming regular
expressions containing letters (from the sequence) or numbers, which are indexes of
registers containg strings. The aim is to minimize the length of the RE, taking
into account the lengths of the strings in the registers plus the markers retained in
the sequence. For example, if KKPAA is repeated 3 times in the sequence, it can be
placed in the register and three index numbers placed in its stead in the sequence.
The net saving from the original 15 characters is 7. AA needs to be found 3 times
for there to be a saving of 1 letter. In general, if N is the number of repetitions
of a string of length LEN, then placing it in a register will effect a saving
of (N-1) * LEN - N. 

Later: Poly-aa (also called homo-aa) treated differently by reps_scoring function.
It is assumed that each letter can also have a number of repetitions as a superscript
(typically just 1).

From V1.31, introduce separate minimum lengths for repetitions (non poly-aa) and
stutters (poly-aa). Rather than complicating the code for get_baselength and iterate_joins,
both reps and stutters are collected as before without distinction, with the cull only
being made (if necessary) in function rep_dict_to_reps_list (called by tile_string).


Principal data structures:
rep_dict maps from the string length, to (repeated) strings of that length, which in turn
	 map to the lists of slices and a boolean, indicating whether the string
	 is homo-aa, ie <strlen> -> <str> -> ([<slice>], <is-homo-aa)
	 After remove_self_occlusion, the structure changes to add scores, ie
	 <strlen> -> <str> -> (<score>, [<slice>], <is-homo-aa>)
reps_list (used in tile_string on) lists the positive scoring repeats in order of
	  descending score. Unlike earlier version of the program, reps_list is just a
	  list of integer indexes (max: reps_list_count-1). The information is now in:
reps_list_map: Which maps from the indexes to (<score>, <str>, <slicelist>)
		The reason for the change is that it allows a compact downstream
		representation of the slices
a_then_b: Is a square matrix mapping pairs of indexes respresented slicelist tiled in the
	  order of first index then second. The format is:
	  <first index> -> <second index> -> (<score>, <result slicelist>, <result slicemap>)
a_then_best_b: Map from indexes to list of score-index pairs, sorted in order of descending
		score. That is, this map is used to get from one index to the others
		Format: <index> -> [(<score>, <index>)]


"""

import sys, string, os, re, imp
import print_in_cols, find_cmd
import kjbuckets

# Only use this for debugging and performance tuning
import profile, pstats

DEBUG = 0
DEBUG_ANALYSIS = 0
TIMES = 0
PROGRESS = 0
PRINT_HEADER = 0

IDWIDTH = 14  # Max ID length for printing
INTWIDTH = 4

# MAX_GAP_FUN = lambda x: x * x
MAX_GAP_FUN = lambda x: x
			# A small function returning the max gap allowed between repetitions
			# based on the length of the peptide (up front allow experimentation)
DEFAULT_MINREP = 2	# Minimim repeated peptide length (e.g KPAKPA)
DEFAULT_MINSTUT = 3	# Minimim stutted peptide (ie poly-aa) length, eg AAAAA
DEFAULT_MAXLEN = 10	# Largest repeated peptide we are interested in

HORNER_MULT = 101L	# Used to create slice-list ends checksums (reps_scoring_function)

OCCAM_TAX = 1		# Penalty for each additional slicelist after the first so that
			# coverings involving fewer slicelists (substrings) are preferred over
			# those with many
MAX_PAIRS = 50		# Number of top scoring pairs from all_against_all phase that
			# flow through to next (iterative deepening) phase

MIN_BIT_COUNT = {0:6+OCCAM_TAX, 1:2+OCCAM_TAX}
			# Based on the current scoring algorithm, this in the minimum number of
			# bits an additional bit-slice should contribute, depending on whether the
			# string is homo-aa or not (must be consistent with reps_scoring_function_recurse)

BFO = 1			# Biologist Friendly Output (subsequences numbered from 1 and exact
			# ends rather than slice end)

ALL_PEPS_IN_SCORES_ONLY = 1 # If this is set, all the low complexity peptides are listed in 
			    # the scores only summary (though not slices), rather than just 
			    # those found in the best patch

# What IUPAC amino acid code letters are disallowed in proteins
NOT_OLIGO_LEXICON = re.compile("[BJOUXZ]")


# For performance monitoring, count number of calls in first and second passes
# compare_slices_calls = {0:0, 1:0}

"""
It is assumed that the sed script preprocessor lives in the same
directory as the other bits of The POPPs. SRCDIR uses the import search
engine to find popp_create, and thence the directory containing the awk script
(which has replaced earlier - and slower - sed script

The awk script is only used if the EMBOSS application seqret is not installed, 
although preliminary testing suggests that it may in fact be quicker! Therefore,
if you want to force use of the awk script, set FORCE_AWK below to 1
"""
FORCE_AWK = 1
WHOAMI = string.split(os.path.basename(sys.argv[0]), ".py")[0]
SRCDIR= os.path.dirname(imp.find_module(WHOAMI)[1])
INPUT_FILTER = SRCDIR + "/preprocess_swissprot.awk"

prev_ID_DE = None  # used to buffer sequence header line

def is_empty_set(set) :
  return(len(set) == 0)

def EMPTY_SET() :
  return(kjbuckets.kjSet([]))

def init() :
  global MAX_PAIRS
  args = sys.argv
  if len(args) == 1:
    sys.stderr.write("Usage: %s OPTIONS <file containing protein sequence(s)\n" % args[0])
    sys.stderr.write("The options are (order is not relevant):\n")
    sys.stderr.write("\t-minrep <N>  - Minimim repeated peptide length (default %d)\n" % DEFAULT_MINREP)
    sys.stderr.write("\t-minstut <N>  - Minimim stutter peptide (poly-aa) length (default %d)\n" % DEFAULT_MINSTUT)
    sys.stderr.write("\t-maxlen <N>  - Maximum peptide length being sought (default %d)\n" % DEFAULT_MAXLEN)
    sys.stderr.write("\t-scores_only  - A summary form in which only total and highest scoring patch scores are printed\n")
    sys.stderr.write("\t-nopep - Do not print out list of peptides in -scores_only (ie JUST scores)\n")
    sys.stderr.write("\t-min_score <N> -  Only report proteins with at least this score\n")
    sys.stderr.write("\t-pep_content <Pep> <N> - To be reported, the repeats and/or stutters in the sequence\n")
    sys.stderr.write("\t\tcontaining <Pep> must amount to at least <N>, e.g. -pep_content P 10\n")
    sys.stderr.write("\t\tin which sequences are not reported with unless repeats containing P\n")
    sys.stderr.write("\t\tattract a total score at least 10 (min_score also set to be at least this value\n")

    sys.stderr.write("\n")
    sys.exit()

  lengths = {"minrep":DEFAULT_MINREP, "minstut":DEFAULT_MINSTUT, "maxlen":DEFAULT_MAXLEN,
		"min_score":0, "pep_content":None}
  scores_only = 0
  print_pep = 1

  i = 1
  while i < len(args) :
    if args[i][0] == '-' :
      if args[i] in [ "-minrep", "-minstut", "-maxlen", "-min_score"] :
	try:
	  n = int(args[i+1])
	except ValueError:
	  sys.stderr.write("%s: non-integer %s found in place of positive integer\n" % (args[0], args[i+1]))
	  i = i + 1
	  continue
	if n < 2 :
	  sys.stderr.write("%s: Values < 2 are not possible\n" % args[0])
	  sys.stderr.write("\tDefault value %d retained\n" % lengths[args[i][1:]])
	else:
	  lengths[args[i][1:]] = n
	i = i + 2
      elif args[i] == "-max_pairs" :
	try:
	  n = int(args[i+1])
	except ValueError:
	  sys.stderr.write("%s: non-integer %s found in place of positive integer\n" % (args[0], args[i+1]))
	  i = i + 1
	  continue
	MAX_PAIRS = n
	i = i + 2
      elif args[i] ==  "-scores_only" :
	scores_only = 1
	i = i + 1
      elif args[i] ==  "-nopep" :
	print_pep = 0
	i = i + 1
      elif args[i] == "-pep_content" :
	pep = string.upper(args[i+1])
	if NOT_OLIGO_LEXICON.search(pep) :
	  sys.stderr.write("Non natural amino acid code %s entered\n" % pep)
	  sys.exit(1)
	try:
	  n = int(args[i+2])
	except ValueError:
	  sys.stderr.write("%s: non-integer %s found in place of positive integer\n" % (args[0], args[i+2]))
	  sys.exit(1)
	if n <= 0  :
	  sys.stderr.write("Only positive integers possible for min scores for peptide %s\n" % pep)
	  sys.exit(1)
	lengths["pep_content"] = (pep, n)
	i = i + 3
      else :
	sys.stderr.write("Unknown option: %s\n" % args[i])
	sys.exit(1)
    else :
      break

  if i == len(args) :
    sys.stderr.write("%s: Input file name missing\n" % args[0])
    sys.exit(1)
  source_pathname = args[i]
  if not os.path.isfile(source_pathname) :
    sys.stderr.write("%s: Database file %s does not exist\n" % (args[0], source_pathname))
    sys.exit(1)

  if lengths["pep_content"] != None :
    if lengths["min_score"] < lengths["pep_content"][1] :
      lengths["min_score"] = lengths["pep_content"][1]

  pos = string.rfind(source_pathname, '.')
  uncompresses = { "z":"pcat", "Z":"zcat", "gz":"zcat", "bz2":"bzcat"}
  if pos > 0 :
    suffix = source_pathname[pos+1:]
    if uncompresses.has_key(suffix) :
      cmd = "%s %s" % (uncompresses[suffix], source_pathname)
    else :
      cmd = "cat %s" % source_pathname
  else:
    cmd = "cat %s" % source_pathname

  # first see if EMBOSS seqret is installed. If so, use it
  seqret_path = find_cmd.find_cmd("seqret")
  if seqret_path != None and not FORCE_AWK :
    cmd = "%s | %s -filter -supper -osformat fasta -stdout" % (cmd, seqret_path)
  else: 
    is_SP = test_if_SP_format(cmd, source_pathname)
    if  is_SP == None : # problem in determining format
      return(None)
    if is_SP :
      if not os.path.isfile(INPUT_FILTER) :
        sys.stderr.write("%s: Sed input filter %s is not found\n" % (args[0], INPUT_FILTER))
        sys.exit(1)

      cmd = "%s | awk -v DELEN=-1 -f %s" % (cmd, INPUT_FILTER)
    else:  # Only a simple filter is needed for FASTA
      cmd = "%s | sed -e '/^ *$/d'" % cmd

  try:
    infile = os.popen(cmd , 'r')
    input_fname = args[i]
  except :
    sys.stderr.write("%s: cannot open input pipe using filter" % args[0])
    sys.exit(1)

  lengths["baselen"] = min(lengths["minrep"], lengths["minstut"])  # saves recomputation
  return(infile, lengths, scores_only, print_pep)

"""
Read the first line(s) of the input file to see if is in SwissProt format,
or whether it has already been converted to FASTA format.
"""
def test_if_SP_format(cmd, source_fname) :
  # Prematurely closing the pipe will generate a UNIX-level error
  # which is of no consequence
  infile = os.popen(cmd + " 2>/dev/null", 'r')
  line = infile.readline()
  while line != "" :
    line = string.strip(line)
    if line == '' :
      line = infile.readline()
      continue
    if line[0] == '>' :
      infile.close()
      return(0)
    if line[:3] == 'ID ' :
      infile.close()
      return(1)
    sys.stderr.write("Cannot determine whether input file %s has SwissProt or FASTA format\n" % source_fname)
    return(None)


"""
Reads lines of a file that has been structured in FASTA format (probably
as a result of the input filter). Because there is no end of record marker,
the header line of the next record
"""
#
def get_sequence(inpipe) :
  global prev_ID_DE

  line = inpipe.readline()
  if line == "" :  # EOF already seen
    return(None, None, None)
  seq_list = []
  while line != "" :
    line = line[:-1]
    if line[0] == '>' :   # Start of next seq. marks end of previous
      fields = string.split(line)
      IDnext = fields[0][1:]
      DEnext = string.join(fields[2:])
      if prev_ID_DE != None: # Not the header of first sequence
        ID, DE  = prev_ID_DE
        seq = string.join(seq_list, "")
        prev_ID_DE = (IDnext, DEnext)
        return(seq, ID, DE)
      prev_ID_DE = (IDnext, DEnext)
    else :
      seq_list.append(line)
    line = inpipe.readline()

  ID, DE  = prev_ID_DE
  return(string.join(seq_list, "") , ID, DE)


"""
Process all the proteins/sequences in a file, which can be SwissProt format, FASTA
reduced format (ie just a line beginning with > and a name, followed by the sequence
lines, or just the sequence lines
"""
#
def process_file(inpipe, lengths, scores_only, print_pep) :
  # global compare_slices_calls

  if TIMES :
    start_time = os.times()
  seq, ID, DE = get_sequence(inpipe)
  while seq != None : # IE, not EOF 
    if ID[:3] == "ALU" :  # One of the 8 ALU contamination hypothetical proteins
      sys.stderr.write("Contamination protein %s is ignored\n" % ID)
      seq, ID, DE = get_sequence(inpipe)
      continue

    if PROGRESS:
      sys.stderr.write("Protein %s\n" % ID)
      sys.stderr.flush()
    process_a_sequence(seq, lengths, ID, DE, scores_only, print_pep)
    if TIMES :
      finish_time = os.times()
      sys.stderr.write("Times %s User: %0.2f Sys: %0.2f\n\n" % (ID, finish_time[0] - start_time[0],\
							     finish_time[1] - start_time[1]))
      start_time = finish_time
    seq, ID, DE = get_sequence(inpipe)

  

def process_a_sequence(seq, lengths, ID, DE, scores_only, print_pep) :
  rep_dict = get_baselength(seq, lengths["baselen"])
  actual_maxlen = iterate_joins(rep_dict, lengths["baselen"], lengths["maxlen"])
  if DEBUG :
    print "Initial map of repeated strings"
    print_reps(rep_dict, lengths["baselen"], actual_maxlen)

  remove_self_occlusion(rep_dict, lengths["baselen"], actual_maxlen)
  if DEBUG :
    print "Map of repeated strings after overlaps removed and scores added"
    print_reps(rep_dict, lengths["baselen"], actual_maxlen)

  all_groups, reps_list_map = tile_string(seq, rep_dict, lengths, actual_maxlen)
  # print 'all_groups', 
  # print_in_cols.print_in_cols(all_groups, 1, '\t')

  if all_groups == [] :
    if scores_only and lengths["min_score"] == 0 :
      sys.stdout.write("%s %s %s\n" % (string.ljust(ID, IDWIDTH),\
		string.rjust(str(len(seq)), INTWIDTH),\
		string.rjust('0', INTWIDTH)))
    elif lengths["min_score"] == 0 :
      print "%s: total score 0 from sequence length: %d" % (ID, len(seq))
      print
  else :
    if scores_only :
      results = analyse_slice_groups(all_groups, reps_list_map, scores_only, lengths)
      if results != None :
	overall_score, b_p_or_pep_score, best_patch_list = results
	sys.stdout.write("%s %s %s  %s" % (string.ljust(ID, IDWIDTH),\
		string.rjust(str(len(seq)), INTWIDTH),\
		string.rjust(str(overall_score), INTWIDTH),\
		string.rjust(str(b_p_or_pep_score), INTWIDTH)))
	if print_pep :
	  best_patch_list.sort()
	  for k in best_patch_list	:
	    sys.stdout.write("  %s" %  k)
	sys.stdout.write("\n")
    else : # scores plus slicelist
      results = analyse_slice_groups(all_groups, reps_list_map, scores_only, lengths)
      if results != None :
	finalslicelist, overall_score, best_patch, b_p_score, overall_haa_score,\
	  b_p_haa_score, max_single_haa_score, particular_pep_score = results

	print "%s %s" % (ID, DE)
	print "    Total score: %d Best patch-score %d from length: %d" % (overall_score, b_p_score, len(seq))
	print"    Of the total/patch scores, %d and %d are due to poly-aa sequences"\
		% (overall_haa_score+OCCAM_TAX, b_p_haa_score+OCCAM_TAX)
	print "    Best single poly-aa patch %d" % max_single_haa_score
	if lengths["pep_content"] != None: # Looking for particular pep
	  print "    Score of peptides containing %s: %d"\
			% (lengths["pep_content"][0], particular_pep_score)
	# print "\n    Best patch slices: "
	# print_in_cols.print_in_cols(best_patch, 4, "    ")
	# print '\n'
	print_in_cols.print_in_cols(finalslicelist, 4)
	print
	print

# get_baselength is given a string representing the sequence, and returns a dictionary
# containing all the dipeptides and their locations, together with booleans indicating
# whether the sequence is homo-aa and whether any sequences are tandem repeats of siblings
def get_baselength(seq, baselength) :
  newdict = {}
  for i in range(len(seq)-baselength+1) :
    k = seq[i:i+baselength]
    if newdict.has_key(k) :
      newlist = newdict[k][0]
      homo_aa = newdict[k][1]
      tandem_repeats = newdict[k][2]
      newlist.append((i, i+baselength))
      if i == newlist[-1][1] and not homo_aa :
	tandem_repeats = 1
      newdict[k] = (newlist, homo_aa, tandem_repeats)
    else :
      newdict[k] = ([(i,i+baselength)], is_homo_aa(k), 0)
  # Now normalize the lists by removing those with only one element.
  revised_dict = {}
  for k in  newdict.keys() :
    nhits = len(newdict[k][0])
    homo_aa = newdict[k][1]
    if nhits == 1 and not homo_aa :  # Need at least 2 hits unless homo-aa
      continue
    if NOT_OLIGO_LEXICON.search(k) :  # Non natural AA found
      continue
    if nhits > 1 or homo_aa :  # These are overlapping hits, which homo-aa also need
      revised_dict[k] = newdict[k]
  del newdict
  return({baselength:revised_dict})

"""
Given a dictionary which currently has strings of length N, join_strs does an all
against all comparison and will join two strings of length N, e.g. KP and PA
so long as:
1)  the suffix N-1 chars of the first substring is the prefix N-1 chars of the other string
2) there are at least two instances where an instance of the second substring starts 1 character
  after the start of the first substring
"""
def join_strs(rep_dict, curlen) :
  # get list of participating substrings (must have at least two instances!) and create
  # map from prefixes to the substring with those prefixes
  curdict = rep_dict[curlen]
  # print "\nProcessing strings of length", curlen
  # strs = curdict.keys()
  # strs.sort()
  # for s in strs :
    # print s, curdict[s]
  #
  prefix_map = {}
  substrlist = []
  for k in curdict.keys() :
    substrlist.append(k)
    if prefix_map.has_key(k[:curlen-1]) :
      prefix_map[k[:curlen-1]].append(k)
    else :
      prefix_map[k[:curlen-1]] = [k]
  # print "substrlist",  substrlist, "\nprefix_map:"
  # print_in_cols.print_in_cols(prefix_map, 1)
  newdict = {}
  for str1 in substrlist :
    str1_is_tandem = curdict[str1][2]
    if str1_is_tandem :
      continue
    haa_str1 = curdict[str1][1]
    if prefix_map.has_key(str1[1:]) :
      for str2 in prefix_map[str1[1:]] : # only look at successors!
	follow_on_list, follow_on_is_tandem, haa_newstr = find_follow_ons(curdict, str1, str2, haa_str1)
	nhits = len(follow_on_list)
	if nhits > 1 or (nhits == 1 and haa_newstr) :
	  newstr = str1 + str2[-1]
	  newdict[newstr] = (follow_on_list, haa_newstr, follow_on_is_tandem)
  del prefix_map, substrlist
  return(newdict)

"""
find_follow_ons is similar to merge, in that the lists of starting positions 
associated with str1 and str2 are in ascending order, but in this case it is
one sided (only need to look at the list corresponding to str1)
"""
def find_follow_ons(curdict, str1, str2, homo_aa_str1) :
  newlist = []
  i = 0
  j = 0
  tandem_repeat = 0
  ends_of_slices = {}  # Just use as hashed list
  str1len = len(curdict[str1][0])
  str2len = len(curdict[str2][0])
  homo_aa_newstr = homo_aa_str1 and str2[-1] == str1[0]
  #
  while i < str1len and j < str2len :
    start_str1_ix = curdict[str1][0][i][0]
    start_str2_ix = curdict[str2][0][j][0]
    if start_str2_ix <= start_str1_ix :
      j = j + 1
    elif start_str2_ix == start_str1_ix + 1 :  # str2 lengthens str1 by 1aa
      end_str2_ix = curdict[str2][0][j][1]
      newlist.append((start_str1_ix, end_str2_ix))	
      if ends_of_slices.has_key(start_str1_ix) and not homo_aa_newstr :  # follows immediately on (cannot be improved)
	tandem_repeat = 1
      ends_of_slices[end_str2_ix] = 1
      i = i + 1
      j = j + 1
    else :    #  IE  curdict[str2][0][j][0] > curdict[str1][0][i][0]
      i = i + 1
  return(newlist, tandem_repeat, homo_aa_newstr)

"""
Given the ability to join adjacent substrings of given length, which, if repeated,
are added to the repeats dictionary, iterate up the lengths until no further
joins are possible, starting from base length (typically 2)
"""
def iterate_joins(rep_dict, curlen, maxlength) :
  newdict = join_strs(rep_dict, curlen)
  while newdict != {} :
    curlen = curlen + 1
    if curlen > maxlength :
      return(curlen-1)
    rep_dict[curlen] = newdict
    newdict = join_strs(rep_dict, curlen)
  return(curlen)  # rep_dict returned as a side effect

def print_reps(rep_dict, baselength, maxlen) :
  for i in range(baselength, maxlen+1) :
    if rep_dict[i] == {} :
      continue
    print "\nRepeats of length:", i
    print_in_cols.print_in_cols(rep_dict[i], 1)
  print


"""
iterate_joins allows overlapping slices to be entered against strings because one
does not know a prior which slice will be lengthed and ultimately used in a tiling.
However, once the process of growing repeated strings has been completed, overlaps
need to be deleted from the lists of slices. (IE no self occlusion)
NOTE: This is where the end-structure of rep_dict changes to include the score
"""
def remove_self_occlusion(rep_dict, baselength, maxlen) :
  for i in range(baselength, maxlen+1) :
    for k in rep_dict[i].keys():
      newslicelist = [rep_dict[i][k][0][0]]
      endcurhit = newslicelist[0][1]
      for start, end in rep_dict[i][k][0][1:] :
	if start >= endcurhit :  # no overlap
	  newslicelist.append((start, end))
	  endcurhit = end
      haa = rep_dict[i][k][1]
      score, haa_score, posnset, LHSset, RHSset =\
			reps_scoring_function_init(newslicelist, i, haa)
      if score > 0 :    # Only worry about repeats which can improve scores
	rep_dict[i][k] =\
		(score, newslicelist, haa, haa_score, posnset, LHSset, RHSset)
      else :
	del rep_dict[i][k]
  return  # rep_dict, now revised and restructured, is returned via a side effect

"""
centralize the function for scoring the list of repetitions
It is assumed that each token is either a letter and multiple of
(tandem) occurances (typically 1) or dictionary index and multiple
of occurences. IE tandem repeats score a bonus 1 for each repeat.
With each slicelist score are also returned a number and a set;
the number is the diagonal on which the slices sit. The contains
integers representing all the positions covered by the slices.
"""
# 
def reps_scoring_function_init(slicelist, strlen, homo_aa):
  nhits = len(slicelist)
  if nhits == 0 :
    return(-1, -1, None, None, None)
  if homo_aa : 
    if nhits == 1 :
      return(strlen-1, strlen-1, kjbuckets.kjSet(range(slicelist[0][0], slicelist[0][1])),\
		kjbuckets.kjSet([slicelist[0][0]]), kjbuckets.kjSet([slicelist[0][1]-1]))
    score = nhits * strlen - nhits # homo-aa not put in dictionary - no advantage
  else :
    score = (nhits - 1)*strlen - nhits
  prevend = slicelist[0][1]
  start = slicelist[0][0]
  allposnslist = range(start, prevend)
  startslist = [start]
  endslist = [prevend-1]
  for start, end in slicelist[1:] :
    if start == prevend : # immediate repeat
      score = score + 1
    allposnslist = range(start, end) + allposnslist
    startslist.append(start)
    endslist.append(end-1)
    prevend = end
  if homo_aa :
    haa_score = score
  else :
    haa_score = 0;
  return(score, haa_score, kjbuckets.kjSet(allposnslist),\
		kjbuckets.kjSet(startslist), kjbuckets.kjSet(endslist))

def reps_scoring_function_recurse(slicelist, strlen, homo_aa):
  nhits = len(slicelist)
  if nhits == 0 :
    return(-1, -1, None)
  if homo_aa : 
    if nhits == 1 :
      return(strlen-1-OCCAM_TAX, strlen-1-OCCAM_TAX, kjbuckets.kjSet(range(slicelist[0][0], slicelist[0][1])))
    score = nhits * strlen - nhits - OCCAM_TAX  # homo-aa not put in dictionary - no advantage
  else :
    score = (nhits - 1)*strlen - nhits - OCCAM_TAX
  prevend = slicelist[0][1]
  start = slicelist[0][0]
  allposnslist = range(start, prevend)
  for start, end in slicelist[1:] :
    if start == prevend : # immediate repeat
      score = score + 1
    allposnslist = range(start, end) + allposnslist
    prevend = end
  if homo_aa :
    haa_score = score
  else :
    haa_score = 0;
  return(score, haa_score, kjbuckets.kjSet(allposnslist))


"""
test whether a particular protein is homo_aa
"""
#
def is_homo_aa(seq) :
  if seq[0] != seq[-1] :
    return(0)
  if len(seq[0]) == 2 :
    return(1)
  item = seq[0]
  for k in seq[1:-1] :
    if k != item :
      return(0)
  return(1)

# Given a list where identical items are adjacent, remove the duplicates 
def uniq_list(list) :
  if list == [] :
    return([])
  prev = list[0]
  return_list = []
  for item in list[1:] :
    if item != prev :
      return_list.append(prev)  # return last of sequence of identicals
    prev = item
  return_list.append(prev)
  return(return_list)

"""
Given two lists of unique items in ascending order, return three lists: items unique to
list1, items uniq to list2 and common items. IE Unix comm
"""
def list_comm(list1, list2) :
  uniq1 = []
  uniq2 = []
  common = []
  while list1 != [] and list2 != [] :
    if list1[0] < list2[0] :
      uniq1.append(list1[0])
      list1 = list1[1:]
    elif list1[0] > list2[0] :
      uniq2.append(list2[0])
      list2 = list2[1:]
    else :
      common.append(list1[0])
      list1 = list1[1:]
      list2 = list2[1:]
  uniq1 = uniq1 + list1
  uniq2 = uniq2 + list2
  return((uniq1, uniq2, common))


"""
Having created a dictionary of strings, each with a list of slices indicating
where the string is to be found, find the best tiling of the strings onto the
sequence.  That is, slices can be included in the final RE so long as the
component slices are not occluded by existing slices (remember that each slice
will end up as an index. Furthermore, down the track, the strings may also be
REs, e.g containing substitutions, but by this stage only dealing with slices.
Secondly, now that reps_list is just a list of indexes into reps_list_map,
these are no longer sorted according to score. Scoring will now be introduced
during compare_all_pairs, so can be dispensed with above.
"""
#
def tile_string(seq, rep_dict, lengths, actual_maxlen) :
  global BFO
  reps_list_map, reps_list_count= rep_dict_to_reps_list(seq, rep_dict, lengths, actual_maxlen)
  if reps_list_count == 0 : # There are no repeats at all, even at the minimum length
    return([], None)
  isolated_groups = find_isolated_slicelists(reps_list_map, reps_list_count)

  # for group in isolated_groups :
    # print 'Group:', group
    # for reps_map_ix in group :
      # item =  reps_list_map[reps_map_ix]
      # print reps_map_ix, item[0], item[1],item[4],
      # print_in_cols.print_in_cols(item[2], 10, '\t')
    # print

  all_groups = []
  for slicelist_group in isolated_groups :  # For each group of overlapping slicelists
    a_then_b, best_first_tuple, ok_combos, a_then_best_b, postive_scoring_list =\
				compare_all_pairs(slicelist_group, reps_list_map)
    if best_first_tuple != () :	     # Either no low comlexity regions, or none combine
      best_score, best_haa_score, best_reps_ix, best_slice_list, best_slice_map = best_first_tuple
      if best_slice_list == [] :  # Really were no reps of the min size
	continue
      best_path_list = [best_reps_ix]
    else  :
      # print_a_then_b(a_then_b, a_then_best_b, reps_list_map)
      bit_scored_list_tilings = extend_best_pairs(ok_combos, postive_scoring_list,\
					reps_list_map, a_then_b)
      best_slice_list, best_slice_map, best_path_list, best_score, best_haa_score =\
	verify_bitwise_tilings(bit_scored_list_tilings, reps_list_map, a_then_b)
      best_final_pair = best_path_list[:2]

      # print 'best_path_list', best_path_list
      # i = 0
      # while i < len(ok_combos) :
	# if best_path_list == ok_combos[i][1] :
	  # print 'best tiling corresponds to index', i, 'in ok_combos'
	  # break
	# i = i + 1

    all_groups.append((best_score, best_haa_score, best_slice_list, best_slice_map, best_path_list))

  return(all_groups, reps_list_map)

"""
tile_string returns a list of tuples containing the best_score, and corresponding
slice list, slice map and pathlist for each of the patches determined by 
find_isolated_slicelists. If the list is empty, nothing was found and that's it,
but if there where slicelists then these must now be analysed. In particular, 
OCCAM_TAX must be deducted from all bar the largest scoring patch (remember that
the first slicelist in each patch is otherwise scot free, when in fact only a single
slicelist will be untaxed overall). Also need to determine the score for the largest
contiguous set of slices.

Up to V 1.33 first deducted OCCAM_TAX and then coalesced neighboruing patches if
they are sufficiently close (remitting the tax in that case), and passing over
patches which are reduced to 0 score by the tax. This is daft and is now changed,
so that first neighbours are joined (if appropriate), then the tax is deducted
from all bar the largest
"""
def analyse_slice_groups(all_patches, reps_list_map, scores_only, lengths) :
  all_patches.reverse()

  if DEBUG_ANALYSIS :
    print 'all_patches'
    print_in_cols.print_in_cols(all_patches, 1)
    print "\nmaxpatch before coalescing", max(map(lambda x: (x[0], -len(x[2]), x), all_patches))[2]

  # First pass goes through all_patches list deducting OCCAM_TAX from all patches other than
  # the highest scoring. In addition, because patches are simply non-overlapping sets of
  # slice lists neighboring patches can be close. If close enough they should be coalesced

  new_patches = [all_patches[0]]
  best_score, best_haa_score, best_slice_list, best_slice_map, best_path_list = all_patches[0]
  # Keep the next two lines in case I want to return to this method of calculating joins
  prev_patch_end_pos = best_slice_list[-1][1]   # Index of the end of the final slice from
						# the prev patch
  # prev_patch_last_str_len = prev_patch_end_pos - best_slice_list[-1][0]
  for patch in all_patches[1:] :
    best_score, best_haa_score, best_slice_list, best_slice_map, best_path_list = patch

    # maxgap was originally the maximum of the repeat lengths at either end of the
    # patch. This disadvantages patches with short repeats at the ends as they are
    # less likely to be coalesced. From 1.34 just have fixed maxgap (== maxlen)
    # cur_patch_first_str_len = best_slice_list[0][1] - best_slice_list[0][0]
    # maxgap = apply(MAX_GAP_FUN, [max(prev_patch_last_str_len, cur_patch_first_str_len)])

    separation = best_slice_list[0][0] - prev_patch_end_pos
    if separation <= lengths["maxlen"] :  # close enough to be coalesced
      prev_score, prev_haa_score, prev_slice_list, prev_slice_map, prev_path_list = new_patches[-1]
      if DEBUG_ANALYSIS :
	print "\nCoalescing slicelist",
	print_in_cols.print_in_cols(prev_slice_list, 10, '\t')
	print "with slicelist",
	print_in_cols.print_in_cols(best_slice_list, 10, '\t')
      prev_score = prev_score + best_score
      prev_haa_score = prev_haa_score + best_haa_score
      prev_slice_list = prev_slice_list + best_slice_list
      prev_path_list = prev_path_list + best_path_list
      for pair in best_slice_map.keys() :  # Transfer slice -> string mappings
	prev_slice_map[pair] = best_slice_map[pair]
      new_patches[-1] = (prev_score, prev_haa_score, prev_slice_list, prev_slice_map, prev_path_list)
    else :
      new_patches.append(patch)
    prev_patch_end_pos = best_slice_list[-1][1]
    # prev_patch_last_str_len = prev_patch_end_pos - best_slice_list[-1][0]

  max_patch = max(map(lambda x: (x[0], -len(x[2]), x), new_patches))[2]
  if OCCAM_TAX > 0 :
    all_patches = new_patches
    new_patches = []
    for patch in all_patches :
      if patch == max_patch :
	new_patches.append(max_patch)
      else:
	best_score, best_haa_score, best_slice_list, best_slice_map, best_path_list = patch
	best_score = best_score - OCCAM_TAX
	if best_score > 0 :
	  best_haa_score = best_haa_score - OCCAM_TAX # Can go < 0, but this will be ignored later
	  new_patches.append((best_score, best_haa_score, best_slice_list, best_slice_map, best_path_list))

  if DEBUG_ANALYSIS :
    print '\nnew_patches'
    print_in_cols.print_in_cols(new_patches, 1)
    print '\nmax_patch', max_patch
  
  combined_score = 0
  combined_haa_score = 0
  combined_slice_lists = []
  combined_slice_maps = {}
  path_hashed_list = {}  # Used to find set of peps in tiling (saves looking at each slice)
  best_path_list = []
  incr_path = []
  if lengths["pep_content"] != None :
    particular_pep = lengths["pep_content"][0]
  else:
    particular_pep = None
  particular_pep_score = 0

  max_single_haa_score = max_patch[1]  # Highest scoring homo-aa patch (not
					# necessarily within the highest scoring patch
  if particular_pep != None :
    pep_contributed_to_patch = 0
  for patch in new_patches :
    best_score, best_haa_score, best_slice_list, best_slice_map, best_path_list = patch
    if patch[1] > max_single_haa_score :
      max_single_haa_score = patch[1]
    combined_score = combined_score + best_score  # This has had OCCCAM_TAX fixed up properly
    if best_haa_score > 0 :
      combined_haa_score = combined_haa_score + best_haa_score
    combined_slice_lists = combined_slice_lists + best_slice_list
    for pair in best_slice_map.keys() :
	combined_slice_maps[pair] = best_slice_map[pair]# transfer the slice->peptide mapping

    if particular_pep != None :
      pep_contributed_to_this_patch = 0
    for reps_map_ix in patch[-1] : # For each member of path_list
      if ALL_PEPS_IN_SCORES_ONLY :
	path_hashed_list[reps_list_map[reps_map_ix][1]] = 1
      if particular_pep != None :
	if string.find(reps_list_map[reps_map_ix][1], particular_pep) > -1 :
	  particular_pep_score = particular_pep_score + reps_list_map[reps_map_ix][0]
	  pep_contributed_to_this_patch = 1
    if particular_pep != None :
      pep_contributed_to_patch = pep_contributed_to_patch + pep_contributed_to_this_patch

  if particular_pep != None :
    particular_pep_score = particular_pep_score - pep_contributed_to_patch + 1

  if combined_score < lengths["min_score"] :
    return(None)
  if particular_pep != None  and particular_pep_score  < lengths["pep_content"][1] :
    return(None)

  # use directory as hashed list to get members of path-list for best patch
  if not ALL_PEPS_IN_SCORES_ONLY : # Only want best patch peps
    for reps_map_ix in max_patch[-1] : # For each member of best_path_list
      path_hashed_list[reps_list_map[reps_map_ix][1]] = 1

  if scores_only :
    if particular_pep != None : # Looking for particular pep, return score
      return((combined_score, particular_pep_score, path_hashed_list.keys()))
    else : # Otherwise the score of the best patch
      return((combined_score, max_patch[0], path_hashed_list.keys()))

  finalslicelist = []
  # combined_slice_lists.sort()
  for start, end in combined_slice_lists:
    finalslicelist.append((start+BFO, end, combined_slice_maps[(start, end)]))

  b_p_slicelist = []
  for start, end in max_patch[2]:
    b_p_slicelist.append((start+BFO, end, combined_slice_maps[(start, end)]))
  return((finalslicelist, combined_score, b_p_slicelist, max_patch[0], combined_haa_score, max_patch[1], max_single_haa_score, particular_pep_score))


"""
rep_dict_to_reps_list in the first instances, just does that: it converts fromm the
dictionary format of rep_dict, with the primary key and secondary keys being
seq len and seq, to the list-of-tuples formatted reps_list, which has the score as
the first element of each tuple. En passant, slicelist which have large gaps between
slices may be broken up, on the basis that if the strings are short and far apart,
they are far less likely to be genuine repeats rather than happenstances. Down the
track, other elements can be introduced, e.g. homo-aa repeats.
Secondly, breaking up of slicelistlists with long gaps can create multiple
reps_list entries with the same peptide, so repslist will instead be a list
of indexes into a map - which is where the actual slices live
Notice that a map from integer indexs to reps_items is returned. The
items corresponding to the ascending indexes are not sorted, as was the
case in some previous versions, because this is now done in function
find_isolated_slicelists 
"""
#
def rep_dict_to_reps_list(seq, rep_dict, lengths, actual_maxlen) :
  global MAX_GAP_FUN

  reps_list_map = {}
  reps_list_count = 0
  for size in range(lengths["baselen"], actual_maxlen+1) :
    maxgap = apply(MAX_GAP_FUN, [size])
    for k in rep_dict[size].keys() :
      score, slicelist, haa, haa_score, posnset, LHSset, RHSset = rep_dict[size][k]

      # Now finally get around to checking against minrep or minstut, as appropriate
      if haa : # If poly-aa
	if  size < lengths["minstut"] :
	  del slicelist, posnset, LHSset, RHSset
	  continue
      else :
	if  size < lengths["minrep"] :
	  del slicelist, posnset, LHSset, RHSset
	  continue

      newlist = [slicelist[0]]
      i = 1
      large_gap_found = 0
      while i < len(slicelist) :
	if slicelist[i][0] - newlist[-1][1] <= maxgap :  # Not too far away
	  newlist.append(slicelist[i])
	else :  # large gap sepates subsets of slices. Split into sublists
	  large_gap_found = 1
	  newscore, newhaa_score, newposnset, newLHSset, newRHSset =\
				reps_scoring_function_init(newlist, size, haa)
	  if newscore > 0 : # still viable
	    reps_list_map[reps_list_count] =\
			(newscore, k, newlist, haa, newhaa_score,\
				newposnset, newLHSset, newRHSset)
	    reps_list_count = reps_list_count + 1
	  newlist = [slicelist[i]]
	i = i + 1
      # newlist is either duplicate of slicelist or shortened
      if large_gap_found : # => need to score last portion
	newscore, newhaa_score, newposnset, newLHSset, newRHSset =\
				reps_scoring_function_init(newlist, size, haa)
	if newscore > 0 : # unchanged or still viable
	  reps_list_map[reps_list_count] =\
			(newscore, k, newlist, haa, newhaa_score,\
				newposnset, newLHSset, newRHSset)
	  reps_list_count = reps_list_count + 1
      else:  # Otherwise accept original slicelist
	reps_list_map[reps_list_count] =\
		(score, k, slicelist, haa, haa_score, posnset, LHSset, RHSset)
	reps_list_count = reps_list_count + 1

  return(reps_list_map, reps_list_count)


"""
The dictionary of string-slicelist tuples produced by rep_dict_to_reps_list
is now scanned to see whether there are isolated patches of overlapping
slicelists. In particular, if there is a single, isolated slicelist, that can
be accepted immediately as a set of tiles and removed from the reps_list.
More likely, groups of overlapping slicelists can be tiled independently
of others.
This works a treat for large proteins which have numerous small patches due to
their size, but nothing of any consequence.
Builds a list of tuples contain the group endpoints and a list of reps_items
in the group
"""
#
def find_isolated_slicelists(reps_list_map, reps_list_count) :
  global _reps_list_map  # just for the sort
  slice_index_pair_list = []
  for i in range(reps_list_count) :
    slice_index_pair_list.append((reps_list_map[i][2], i))
  slice_index_pair_list.sort(cmp_slicelist_index_pairs)
  # print 'slice_index_pair_list'
  # print_in_cols.print_in_cols(slice_index_pair_list, 1)
  slicelist = slice_index_pair_list[0][0]
  endpoints = [(slicelist[0][0], slicelist[-1][1], [slice_index_pair_list[0][1]])]
  for slicelist, reps_item_ix in slice_index_pair_list[1:] :
    start = slicelist[0][0]
    end = slicelist[-1][1]
    group_start, group_end, group = endpoints[-1]
    if end < group_start  : # comes before current group => new group
      endpoints.append((start, end, [reps_item_ix]))
    else : # slicelist end <= group_end due to sort, so add to group
      group.append(reps_item_ix)
      if start < group_start : # does start extend group?
	group_start = start
      endpoints[-1] = (group_start, group_end, group)

  # previous versions sorted the group members, but this is
  # actually not required because ok_combos resorted by compare_all_pairs
  # for use in iterated_over_pairs
  sorted_isolated_groups = []
  _reps_list_map = reps_list_map
  for dontcare0, dontcare1, group in endpoints :
    group.sort(cmp_reps_item_by_sets)
    sorted_isolated_groups.append(group)

  del _reps_list_map
  return(sorted_isolated_groups)

      
# sort by decreasing endpoint
def cmp_slicelist_index_pairs(pair0, pair1) :
  end0 = pair0[0][-1][1]
  end1 = pair1[0][-1][1]
  if end0 > end1 :
    return(-1)
  if end0 < end1 :
    return(1)
  start0 = pair0[0][0][0]
  start1 = pair1[0][0][0]
  if start0 < start1 :
    return(-1)
  return(start1 > start0)

# sorted by decreasing coverage of the source string as evidenced by the cardinality
# of the posn_sets
def cmp_reps_item_by_sets(rix0, rix1) :
  nitemset0 = len(_reps_list_map[rix0][5])
  nitemset1 = len(_reps_list_map[rix1][5])
  if nitemset0 > nitemset1 :
    return(-1)
  return(nitemset1 > nitemset0)
    

"""
To limit the factorial (exponential!) behaviour, compare_all_pairs does an
all against all comparison of the slicelists N*(N-1) because order is relevant so
only self comparisons can be avoided. A matrix shaped map is constructed
so that if peptides A followed by B are being considered, then the selection
of peptides C to follow B need only consider those that have a nonzero score
when they succeed both A and B.
If all combinations yield no improvements in value, the best (score, slicelist, slicemap)
tuple is returned (else the empty tuple)
Finally, it is also possible that every combination of two slicelists is worse than
the best single slicelist, in which case, the single slicelist is returned (more
combinations will only make things worse over the same slicelist group
"""
#
def compare_all_pairs(reps_list, reps_list_map) :
  global OCCAM_TAX
  a_then_b = {}
  a_then_best_b = {}
  best_first_score = 0	# Score for best single slicelist
  best_first_haa_score = 0	# Contribution to best score from homo-aa
  best_pair_score = 0	# Score for best pair of slicelists
  best_first_set_card = len(reps_list_map[reps_list[0]][5])  # | largest posn_set |
  best_first_slice_list = []
  best_first_slice_map = {}
  positive_score_set = {}  # keep counts of solid hits - need at least 2
  best_reps_ix = -1
  ok_combos = []  # List of slicelist pairs which result in improved scores
  head_ok_combos = []   # head of the ok_combos list stop when this stabilizes
  for first in reps_list :
    if not a_then_b.has_key(first) :  # if already initialized, don't clobber it!
      a_then_b[first] = {}
    a_then_best_b[first] = []   # don't need to check this so long as only -1 values
				# are added in the prior pass
    first_slice_list = reps_list_map[first][2]
    first_slice_map =  add_to_slice_map({}, first_slice_list, reps_list_map[first][1])
    first_score = reps_list_map[first][0]
    first_haa_score = reps_list_map[first][4]
    first_start = first_slice_list[0][0]
    first_length = len(first_slice_list)
    first_posn_set = reps_list_map[first][5]
    card_first_posn_set = len(first_posn_set)
    #
    # En passant, this finds the best single slicelist. This should generally
    # be the first in reps_list (which is sorted by posn_set), but posn_set ~= score
    if first_score > best_first_score : 
      best_first_slice_list = first_slice_list
      best_first_slice_map = first_slice_map
      best_first_score = first_score
      best_first_haa_score = first_haa_score  # IE either 0 or == first_score (if homo-aa)
      best_reps_ix = first
    lower_triangle = 1
    for second in reps_list:
      if first == second :
	lower_triangle = 0
	continue

      # Already been dealt with!
      if a_then_b[first].has_key(second) :
	continue

      # Even if this does jive with the existing slices, the additional score
      # is no greater than the penalty for each additional slicelist (after first)
      if reps_list_map[second][0] <= OCCAM_TAX :	
	a_then_b[first][second] = (-1, -1, None, None, None)
	continue

      second_slice_list = reps_list_map[second][2]
      second_length = len(second_slice_list)
      second_posn_set = reps_list_map[second][5]
      second_LHS_set = reps_list_map[second][6]
      second_RHS_set = reps_list_map[second][7]
      second_k = reps_list_map[second][1]
      second_haa = reps_list_map[second][3]

      LHSides = second_LHS_set - first_posn_set	# LHS set (ie slice starts)
      nslices_added = len(LHSides)
      if nslices_added < 2 and (not second_haa or nslices_added < 1) :
	# print "LHS Slice bit-test catches match", reps_list_map[first][1], first_slice_list, 'versus', second_k, second_slice_list
	a_then_b[first][second] = (-1, -1, None, None, None)
	continue

      RHSides = second_RHS_set - first_posn_set	# RHS set (ie slice ends)
      nslices_added = len(RHSides)
      if nslices_added < 2 and (not second_haa or nslices_added < 1) :
	# print "RHS Slice bit-test catches match", reps_list_map[first][1], first_slice_list, 'versus', second_k, second_slice_list
	a_then_b[first][second] = (-1, -1, None, None, None)
	continue

      slice_end_incr = len(second_k) - 1
      nslices_added = 0
      for slice in LHSides.items() :
	nslices_added = nslices_added +  RHSides.member(slice + slice_end_incr)
      if nslices_added < 2 and (not second_haa or nslices_added < 1) :
	a_then_b[first][second] = (-1, -1, None, None, None)
	continue


      n_slice_bits_added = nslices_added * (slice_end_incr + 1)
      n_bits_added = len(second_posn_set - first_posn_set)
      if n_bits_added < n_slice_bits_added or n_slice_bits_added < MIN_BIT_COUNT[second_haa] :
	# print "Bitwise improvement", n_bits_added, "insufficient for", reps_list_map[first][1], first_slice_list, 'versus', second_k, second_slice_list, second_haa
	a_then_b[first][second] = (-1, -1, None, None, None)
	continue

      # Testing here for combinations that are unlikely to turn out to be the best, but
      # make be required during the recursive search. For this reason, a match for
      # this test results in a_then_b being given the value 0 (rather than 1)
      # and a_then_best_b being given an estimated score which is 1/4 the cardinality
      # If the pair are encountered later (unlikely), the real call to compare_slices
      #  will be made
      #

      total_posn_set_card = card_first_posn_set + n_slice_bits_added
      if total_posn_set_card < best_first_set_card :
	# print "Total posn_set length %d for %s %s + %s %s less than %d" % (total_posn_set_card, reps_list_map[first][1], first_slice_list, second_k, second_slice_list, best_first_set_card)
	a_then_b[first][second] = (0, 0, None, None, None)
	a_then_best_b[first].append((total_posn_set_card / 4, second))
	positive_score_set[second] = 1
	continue

      # print 'Stage 1 Comparing:', reps_list_map[first][1], first_slice_list, ' with:', reps_list_map[second][1], second_slice_list,
      item_score, item_haa_score, new_slice_list, item_posn_set, item_slice_map =\
		compare_slices(second_slice_list, first_slice_list, first_slice_map, second_k, second_haa, 0)
      # print 'Score:', item_score,
      new_score = item_score + first_score
      new_haa_score = item_haa_score + first_haa_score
      if item_score <= 0 :
	a_then_b[first][second] = (-1, -1, None, None, None)
	# print
      # Only record symmetrical order of two peptides if they result in different slicelists
      # elif not lower_triangle or a_then_b[second][first][2] != new_slice_list :
      elif not lower_triangle or new_score >= a_then_b[second][first][0] :
	new_posn_set = item_posn_set + first_posn_set
	a_then_b[first][second] = (new_score, new_haa_score, new_slice_list, new_posn_set,  item_slice_map)
	a_then_best_b[first].append((new_score, second))
	ok_combos.append((new_score, [first, second]))
	positive_score_set[second] = 1
	if new_score > best_pair_score :  # only need check when done for first time or different
	  best_pair_score = new_score
	# special case of completely independent slicelists (no overlaps at all)
	if len(new_slice_list) == first_length + second_length :
	  add_second(a_then_b, second, first, (-1, -1, None, None, None))
      else :  # mostly indept slicelists, but same joint slicelist
	a_then_b[first][second] = (-1, -1, None, None, None)

    if a_then_best_b[first] != []  : # some slices had positive scores this round
      a_then_best_b[first].sort()  # sort by score
      a_then_best_b[first].reverse()  # sort by decreasing score
      ok_combos.sort()
      if ok_combos[-MAX_PAIRS:] == head_ok_combos :  # sorts in ascending order!!!
	break
      head_ok_combos = ok_combos[-MAX_PAIRS:]

  if ok_combos == []  or best_first_score > best_pair_score :
    return({}, (best_first_score, best_first_haa_score, best_reps_ix, best_first_slice_list, best_first_slice_map), [], {}, [])
  # ok_combos already sorted above, but in ascending order, so reverse it
  ok_combos.reverse()
  # print 'length of ok_combos before initial truncation', len(ok_combos)
  ok_combos = ok_combos[:MAX_PAIRS]
  postive_scoring_list = []
  for i in reps_list :
    if positive_score_set.has_key(i) :
      postive_scoring_list.append(i)
  # print 'ok_combos'
  # print_in_cols.print_in_cols(ok_combos, 8)
  return(a_then_b, (), ok_combos, a_then_best_b, postive_scoring_list)

# This assumes map exists and has been initialized to a map
def add_second(map, first, second, value) :
  try:
    map[first][second] = value
  except KeyError:
    map[first] = {second:value}

"""
Given the list of test scoring slice-list pairs (ok_combos), and the list of
all currenty active slice_lists (postive_scoring_list), return a revised
list of score-list tuples, where the lists of slice-list indexes are found by
adding more and more slices to each initial pair
extend_best_pairs adds an extra tiling levels in a breadth first fashion
"""

def extend_best_pairs(ok_combos, postive_scoring_list, reps_list_map, a_then_b) :
  bit_scored_list_tilings = []
  final_bit_scored_list_tilings = []
  continue_trawling = 0
  for dontcare, tiling in ok_combos :
    first_slice, second_slice = tiling   # each tiling begins with the intial pair
    bit_set = a_then_b[first_slice][second_slice][3]
    score = len(bit_set)
    test_set = kjbuckets.kjSet(postive_scoring_list)
    if test_set.member(first_slice):
      del test_set[first_slice]
    if test_set.member(second_slice):
      del test_set[second_slice]

    new_score, new_test_set, new_tiling, new_bit_set =\
		trawl_slice_list_set(test_set, reps_list_map, tiling, bit_set)
    if new_score <= 0 :
      final_bit_scored_list_tilings.append((score, tiling))
    else :
      # sys.stdout.write('Extend first stage %s (%d) %s (%d)\n' % (tiling, score, new_tiling, score + new_score))
      bit_scored_list_tilings.append((score + new_score, new_tiling, new_test_set, new_bit_set))
      continue_trawling = 1

  while continue_trawling  and bit_scored_list_tilings != [] :
    # if len(bit_scored_list_tilings) >= 9 :
      # bit_scored_list_tilings.sort()
      # bit_scored_list_tilings.reverse()
      # new_top = 2 * len(bit_scored_list_tilings)/3
      # for score, tiling, test_set, bit_set in bit_scored_list_tilings[new_top:] :
	# final_bit_scored_list_tilings.append((score, tiling))
      # print "bit_scored_list_tilings shortened from", len(bit_scored_list_tilings),
      # bit_scored_list_tilings = bit_scored_list_tilings[:new_top]
      # print "to", len(bit_scored_list_tilings), "elements"
    
    new_bit_scored_list_tilings = []
    bit_scored_list_tilings.sort()
    bit_scored_list_tilings.reverse()
    continue_trawling = 0
    for score, tiling, test_set, bit_set in bit_scored_list_tilings :
      new_score, new_test_set, new_tiling, new_bit_set =\
		trawl_slice_list_set(test_set, reps_list_map, tiling, bit_set)
      if new_score <= 0 :
	final_bit_scored_list_tilings.append((score, tiling))
      else :
	new_bit_scored_list_tilings.append((score + new_score, new_tiling, new_test_set, new_bit_set))
	# sys.stdout.write('Extend next stage %s (%d) %s (%d)\n' % (tiling, score, new_tiling, score + new_score))
	continue_trawling = 1

    bit_scored_list_tilings = new_bit_scored_list_tilings

  # print 'bit_scored_list_tilings before sorting'
  # print_in_cols.print_in_cols(final_bit_scored_list_tilings, 4)
  final_bit_scored_list_tilings.sort()
  final_bit_scored_list_tilings.reverse()
  # print 'final_bit_scored_list_tilings'
  # print_in_cols.print_in_cols(final_bit_scored_list_tilings, 4)
  return(final_bit_scored_list_tilings)

# trawl through the set of active slicelists with respect to the current tiling and add the
# slicelist that best improves the bitwise score, returning the revised score, tiling,
# active slicelist list and bitset
def trawl_slice_list_set(SLset, reps_list_map, tiling, bit_set) :
  cur_best_slice_ix = None	# Index of best scoring slicelist w.r.t. current bitset
  cur_best_incr_score = 0	# Score for the best scoring slicelist
  cur_best_slices = None
  new_test_set = EMPTY_SET()
  for i in SLset.items() :
    test_item = reps_list_map[i]
    item_haa = test_item[3]

    LHSides = test_item[6] - bit_set   	# LHS set (ie slice starts)
    nslices_added = len(LHSides)
    if nslices_added < 2 and (not item_haa or nslices_added < 1) :
      continue

    RHSides = test_item[7] - bit_set   	# RHS set (ie slice ends)
    nslices_added = len(LHSides)
    if nslices_added < 2 and (not item_haa or nslices_added < 1) :
      continue
	
    str_len = len(test_item[1])
    slice_end_incr = str_len - 1		# length of string (-1)

    # Check that the LHS has a corresponding RHS and that all the bits in betwee are
    # also present (ie no case of smaller string wholy fitting within a longer one
    slices_added = []
    for slice in LHSides.items() :
      if RHSides.member(slice + slice_end_incr) and\
		len(kjbuckets.kjSet(range(slice, slice + str_len)) - bit_set) == str_len :
	slices_added.append((slice, slice + str_len))
    nslices_added = len(slices_added)
    if nslices_added < 2 and (not item_haa or nslices_added < 1) :
      del slices_added
      continue

    n_slice_bits_added = nslices_added * str_len
    if n_slice_bits_added < MIN_BIT_COUNT[item_haa] :
	del slices_added
	continue

    # print "For tiling %s, may add %i with incr score %d, LHS %s, RHS %s" % (tiling, i, n_slice_bits_added, LHSides, RHSides)
    if n_slice_bits_added >cur_best_incr_score :
	cur_best_incr_score = n_slice_bits_added
	cur_best_slice_ix = i
	cur_best_slices = slices_added

    new_test_set.add(i)

  if cur_best_slice_ix == None :
    return(-1, None, tiling, bit_set)

  tiling.append(cur_best_slice_ix)
  for start, end in cur_best_slices :
    bit_set = bit_set + kjbuckets.kjSet(range(start, end))
  del new_test_set[cur_best_slice_ix]
  return(cur_best_incr_score, new_test_set, tiling, bit_set)

"""
Having extended the pairs using bit comparisons, verify the tilings created
by that process. Remember that bitwise scoring is only an approximation the the
actual scoring function.
"""
def verify_bitwise_tilings(bit_scored_list_tilings, reps_list_map, a_then_b) :
  best_score = 0
  best_details = None
  for bitscore, tiling_list in bit_scored_list_tilings :
    score, haa_score, slice_list, dontcare, slice_map = a_then_b[tiling_list[0]][tiling_list[1]]
    for next in tiling_list[2:] :
      slice_item = reps_list_map[next]
      next_str = slice_item[1]
      next_list = slice_item[2]
      next_haa = slice_item[3]
      next_score, next_haa_score, slice_list, dontcare1, slice_map =\
	compare_slices(next_list, slice_list, slice_map, next_str, next_haa, 1)
      if next_score <= 0 : # This should not happen!!
	sys.stdout.write("The bitwise tiling %s fails when %d is added\n" % (tiling_list, next))
	break
      score = score + next_score
      haa_score = haa_score + next_haa_score
    else: # IE nothing untoward happened
      # print 'Verify', tiling_list, score, haa_score, 'original bitscore', bitscore
      if score > best_score :
	best_details = (slice_list, slice_map, tiling_list, score, haa_score)
	best_score = score

  if best_details == None :
    print 'No best tiling left!!!'
  # else :
    # print 'best tiling', best_details[2]
  return(best_details)


# A print function for a_then_b (debugging purposes only)
def print_a_then_b(a_then_b, a_then_best_b, reps_list_map) :
  print 'a_then_b and a_then_best_b'
  for first in a_then_b.keys() :
    sys.stdout.write("a_then_best_b[%d=%s] = %s\n" % (first, reps_list_map[first][1], a_then_best_b[first]))
    for second in a_then_b[first].keys() :
      if first == second :
	continue
      print reps_list_map[first][1], reps_list_map[second][1], a_then_b[first][second][0], a_then_b[first][second][2]
  print


# for each slice noted against a string, add the slice to the slice map
# pointing to the string
def add_to_slice_map(slice_map, okslices, beststr) :
  for s in okslices :
    slice_map[s] = beststr
  return(slice_map)

# see if enough of the new slices fit in with the existing pattern of new slices
# and return a score for those that do! 
# NOTE that the returned score is incremental, as is the set, but the slicelist and the
# slice_map combine the original and new slicelists.
def compare_slices(new_slices, old_slices, slice_map, rep_str, haa_str, which_pass) :
  # compare_slices_calls[which_pass] = compare_slices_calls[which_pass] + 1
  okslices = []
  finalslices = []
  i = 0
  j = 0
  nlen = len(new_slices)
  olen = len(old_slices)
  while i < nlen and j < olen :
    if new_slices[i][1] <= old_slices[j][0] :
      okslices.append(new_slices[i])
      finalslices.append(new_slices[i])
      i = i + 1
    elif old_slices[j][1] <= new_slices[i][0] :
      finalslices.append(old_slices[j])
      j = j + 1
    else :
      i = i + 1
  if i < nlen :  # new slices follow all the old ones
    okslices = okslices + new_slices[i:]
    finalslices = finalslices + new_slices[i:]
  else :
    finalslices = finalslices + old_slices[j:]
  okscore, haa_score, ok_posn_set = reps_scoring_function_recurse(okslices, len(rep_str), haa_str)
  if okscore <= 0 :
    return(okscore, okscore, None, None, None)
  return(okscore, haa_score, finalslices, ok_posn_set, add_to_slice_map(slice_map, okslices, rep_str))

    
def run() :
  inpipe, lengths, scores_only, print_pep = init()
  sys.stderr.write('minrep %d, minstut %d, maxlength %d, MAX_PAIRS %d, OCCAM_TAX: %d\n' %\
				(lengths["minrep"], lengths["minstut"], lengths["maxlen"], MAX_PAIRS, OCCAM_TAX))
  if PRINT_HEADER and  scores_only :
    if lengths["pep_content"] != None:
      print "Tsc is total score; PSc is the score for peptide %s"\
		% lengths["pep_content"][0]
    else:
      print "Tsc is total score; PSc is the score from the best path"
    if ALL_PEPS_IN_SCORES_ONLY :
      which_patches = "all patches"
    else:
      which_patches = "best patch"
    print "%s %s %s  %s   Peps from %s"\
	% (string.center("ID", IDWIDTH), string.center("Len", INTWIDTH),
	   string.center("TSc", INTWIDTH),  string.center("PSc", INTWIDTH), which_patches)
  process_file(inpipe, lengths, scores_only, print_pep)

if __name__ == "__main__" :
  run()
  # profile.run("run()", "prof.out")
  # p = pstats.Stats("prof.out")
  # p.strip_dirs().sort_stats("cumulative").print_stats()
