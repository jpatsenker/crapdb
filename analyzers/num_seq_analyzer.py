from analyzers.sewageanalyzer import SewageAnalyzer
from aux import logtools


class NumSeqAnalyzer(SewageAnalyzer):
	"""
	Calculates number of sequences in the clean and dirty files and outputs to log and analysis file
	"""

	__name__ = "NUMBER_SEQUENCES_ANALYZER"

	__log_fil__ = None
	__mess_fil__ = None



	def __init__(self, lfil = None, mfil = None):
		"""
		Constructor
		:param lfil: log filename
		:param mfil: file with all messy sequences (the dirty file)
		:return:
		"""
		super(SewageAnalyzer, self).__init__()
		self.__log_fil__ = lfil
		self.__mess_fil__ = mfil

	def analyze_crap(self, input_file, analysis_file, graphic=False):
		"""
		Analyze for number of sequences
		:param input_file:
		:param analysis_file:
		:param graphic:
		:return:
		"""
		#count how many clean sequences are left
		with open(input_file, "r") as input_stream:
			every = input_stream.read()
			stuff = every.split("\n")
			num_seq = int(len(stuff)/2)
		with open(analysis_file, "w") as analysis_stream:
			analysis_stream.write(str(num_seq))
		if self.__log_fil__ is not None:
			logtools.add_line_to_log(self.__log_fil__, "Number of non-CRAP sequences left: " + str(num_seq))
		#count how many CRAP sequences have been found, if the file is presented
		if self.__mess_fil__ is not None:
			with open(self.__mess_fil__, "r") as input_stream:
				every = input_stream.read()
				stuff = every.split("\n")
				mess_seq = int(len(stuff)/2)
			logtools.add_line_to_log(self.__log_fil__, "Number of CRAP sequences currently: " + str(mess_seq))