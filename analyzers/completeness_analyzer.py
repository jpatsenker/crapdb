from sewageanalyzer import SewageAnalyzer
from model.fasta_tools import FastaReader
from model.fasta_tools import FastaWriter

#TODO: FINISH THIS ANALYZER
class CompletenessAnalyzer(SewageAnalyzer):
	"""
	Analyzer the genome for completeness, whether it satisfies a core set of genes specified by the self.__complete_set__ fasta file
	"""

	__name__ = "Completeness Analyzer"

	def __init__(self, completeSet):
		self.__complete_set__ = completeSet
		super(CompletenessAnalyzer, self).__init__()

	def analyze_crap(self, input_file, analysis_file, graphic):
		numSeq = 0

		namedFile = input_file + ".named"

		#TODO: run gene name assignment

		#TODO: here check if the assignment matches to a complete set, print results to analyzer
		with FastaReader(namedFile) as namedReader:
			with FastaReader(self.__complete_set__) as completeReader:
				querySeq = namedReader.readSequence()
				while querySeq is not FastaReader.EOF:
					referSeq = completeReader.readSequence()
					while referSeq is not FastaReader.EOF:
						if querySeq == referSeq:
							pass