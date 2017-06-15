from abc import ABCMeta, abstractmethod

class SewageFilter:
	"""
	The Filter super class, build any filter that takes in an input file of sequences and writes into a clean file with good sequences and a dirty file with CRAP sequences
	"""
	__metaclass__ = ABCMeta

	__name__ = None

	def __init__(self):
		self.__logfile__ = None



	@abstractmethod
	def filter_crap(self, input_file, output_file, diagnostics_file):
		"""
		Method for filtering proteomes based on certain statistic (i.e. redundancy, complexity, fission/fusion, lengths, etc)
		:param input_file: name of input fasta file
		:param output_file: name of output fasta file that is cleaned of extra sequences
		:param diagnostics_file: name of diagnostics file with all problematic sequences (appended to)
		:return:
		"""
		pass


	def get_name(self):
		"""
		Getter for name, (for logging)
		:return:
		"""
		return self.__name__

	def set_logfile(self, logfile):
		"""
		Setter for logfile, for flexibility
		:param logfile: string as log file
		:return:
		"""
		self.__logfile__ = logfile

	def has_logfile(self):
		"""
		Check if log file is set
		:return: boolean whether log file is set
		"""
		return self.__logfile__ is not None

class BrokenFilterError(Exception):
	"""
	A Custom Exception that writes which kind of filter has broken (good for logging)
	Raise this when another specific error after logging the error
	"""
	def __init__(self, fil):
		super(BrokenFilterError, self).__init__("The filter <" + str(fil) + "> has broken!!!")