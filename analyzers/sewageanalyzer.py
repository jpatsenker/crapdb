from abc import ABCMeta, abstractmethod

class SewageAnalyzer:
	"""
	The Analyzer superclass
	This module takes in an input file, and writes to an analysis file and/or generates a graphic
	Does not perform "filtering"
	"""
	__metaclass__ = ABCMeta

	__name__ = None

	def __init__(self):
		super(SewageAnalyzer, self).__init__()



	@abstractmethod
	def analyze_crap(self, input_file, analysis_file, graphic):
		"""
		:param input_file: input as current state of fasta file
		:param analysis_file: output name for graphic/csv file
		:param graphic: boolean whether to generate graphic
		:return:
		"""
		pass

	def get_name(self):
		return self.__name__