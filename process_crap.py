from sequence_length_filter import SeqLengthFilter
from sewagesystem import SewageSystem

ss = SewageSystem()

len_filter = SeqLengthFilter(30, 30000)

iFile = None
oFile = None
dFile = None
tDir = None

ss.add_filter(len_filter)

ss.filter_crap(iFile, oFile, dFile, tDir)