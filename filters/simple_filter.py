from filters.sewagefilter import SewageFilter
from aux import logtools


class SimpleFilter(SewageFilter):
	"""
	This is run after the fasta check filter. Because the fasta checker replaces bad characters with 'x' this filter is ALWAYS necessary after the Fasta Filter.
	Also checks for manual 'X' characters set by design. Too many in a sequence means it is likely incomplete
	Checks for M in the beginning if parameter set
	TODO: add this filtering after fasta checker, this is unstylistic
	"""

	__name__ = "SIMPLE_FILTER"

	__ms__ = None
	__xs__ = None


	def __init__(self, ms, xs):
		"""
		Initialize this filter
		:param ms: boolean whether or not the filter should make sure there is a start codon (M) to start the sequence
		:param xs: integer as how many consecutive 'X's (manual) will be tolerated at most in a sequence
		:return:
		"""
		super(SimpleFilter, self).__init__()
		self.__ms__=ms
		self.__xs__=xs

	def filter_crap(self, input_file, output_file, diagnostics_file):
		"""
		Filter the fasta checker out
		:param input_file:
		:param output_file: clean
		:param diagnostics_file: dirty
		:return:
		"""
		#log
		logtools.add_line_to_log(self.__logfile__, "---Filtering out sequences with more than " + str(self.__xs__) + " Xs")
		if self.__ms__:
			logtools.add_line_to_log(self.__logfile__, "---Filtering out sequences that don't start with M")
		#make sure output is ready
		open(output_file, "w").close()
		#open input stream
		with open(input_file, "r") as input_stream:
			#loop over the fasta file
			line = input_stream.readline()
			while line:
				sequence = input_stream.readline()
				sequence = sequence.rstrip("\n")
				#check for chars filtered out by fasta-checker
				if 'x' in sequence:
					#write to dirty
					with open(diagnostics_file, "a") as diag_stream:
						diag_stream.write(line.rstrip("\n") + " Invalid Characters in Sequence \n" + sequence + "\n")
					line = input_stream.readline()
					continue
				#check for M in the beginning in case the parameter is set
				if sequence[0] != 'M' and self.__ms__:
					#write to dirty
					with open(diagnostics_file, "a") as diag_stream:
						diag_stream.write(line.rstrip("\n") + " Sequence Does Not Start With M \n" + sequence + "\n")
					line = input_stream.readline()
					continue
				#check for 'X's consecutive (notation for mystery codons)
				if 'X'*(self.__xs__ + 1) in sequence:
					# write to dirty
					with open(diagnostics_file, "a") as diag_stream:
						diag_stream.write(line.rstrip("\n") + " Sequence Has Too Many Xs \n" + sequence + "\n")
					line = input_stream.readline()
					continue
				#if all tests check out, write to clean
				with open(output_file, "a") as out_stream:
					out_stream.write(line + sequence + "\n")
				#iterate
				line = input_stream.readline()