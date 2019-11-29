from abc import ABCMeta, abstractmethod
import sys
import os

from filters.sewagefilter import SewageFilter
from filters.sewagefilter import BrokenFilterError
from model.fasta_tools import FastaReader
from model.fasta_tools import FastaWriter
from aux import hmmer_tools
import random
from aux import logtools

class AlignmentInfo:
	"""
	A class that stores Hmmer output in Info objects, for easier accessibility and parsing of Hmmer outputs
	Hmmer computes alignment between a query set of sequences and a target set, giving an e-value for alignments between pairs of Query and Target sequences.
	This class stores a single alignment as designated by Hmmer, between 2 sequences
	"""
	def __init__(self, qf, qt, tf, tt, e):
		self.__queryFrom__ = qf
		self.__queryTo__ = qt
		self.__targetFrom__ = tf
		self.__targetTo__ = tt
		self.__evalue__ = e
	'''
	Getters
	'''
	def getQueryFrom(self):
		"""
		Returns index as beginning of aligned query subsequence in query sequence
		"""
		return self.__queryFrom__
	def getQueryTo(self):
		"""
		Returns index as end of aligned query subsequence in query sequence
		"""
		return self.__queryTo__
	def getTargetFrom(self):
		"""
		Returns index as beggining of aligned target subsequence in target sequence
		"""
		return self.__targetFrom__
	def getTargetTo(self):
		"""
		Returns index as end of aligned target subsequence in target sequence
		"""
		return self.__targetTo__
	def getEValue(self):
		"""
		Returns EValue of alignment
		"""
		return self.__evalue__
	'''
	Setters
	'''
	def setQueryFrom(self, qf):
		self.__queryFrom__ = qf
	def setQueryTo(self, qt):
		self.__queryTo__ = qt
	def setTargetFrom(self, tf):
		self.__targetFrom__ = tf
	def setTargetTo(self, tt):
		self.__targetTo__ = tt
	def setEValue(self, e):
		self.__evalue__ = e
	'''
	Built-In overrides for easier debugging/logging
	'''
	def __str__(self):
		return "{{Query: (" + str(self.__queryFrom__) + "->" + str(self.__queryTo__) + "), Target: (" + str(self.__targetFrom__) + "->" + str(self.__targetTo__) + "), e-value: " + str(self.__evalue__) + "}}"
	def __repr__(self):
		return str(self)


class ConcatEvent:
	"""
	Class for holding onto Fission/Fusion (fF) Events, generalized for both. Used to sort alignment info into "events", which are then deemed dirty or clean
	A Concat Event, contains a main sequence mainseq, and a dictionary of sub sequences subseq. This relationship should be well defined by what kind of ConcatEvent it is
	:specfield mainseq: larger sequence that encompasses all the other sequences
	:specfield subseqs: dictionary of all the smaller sequences mapped to their location in the original string
	"""

	__metaclass__ = ABCMeta
	def __init__(self, mainseq):
		self.__mainseq__ = mainseq
		self.__subseqs__ = {} #dictionary of Sequence -> (Int, Int)

	@abstractmethod
	def getScore(self):
		"""
		Method for getting score of event
		"""
		pass

	def addSubseq(self, subseq):
		"""
		Method for adding subsequence to event
		"""
		if not self.__subseqs__.has_key(subseq):
			self.__subseqs__[subseq] = []

	def setCoords(self, subseq, coordinates):
		"""
		Method for setting coordinates of sequence
		"""
		if self.__subseqs__.has_key(subseq):
			self.__subseqs__[subseq].append(coordinates)
		else:
			raise Exception("Cannot set coordinates for non-existant subsequence " + str(subseq) + " (main sequence: " + str(self.__mainseq__) + ")")

	def getCoords(self, subseq):
		"""
		Method for getting coordinates of subsequence
		"""
		try:
			return self.__subseqs__[subseq]
		except KeyError:
			raise Exception("Cannot get coordinates for non-existant subsequence " + str(subseq) + " (main sequence: " + str(self.__mainseq__) + ")")

	def getSubseqs(self):
		return dict(self.__subseqs__)

	def getMainSeq(self):
		return self.__mainseq__

	def removeSubseq(self, subseq):
		if subseq in self.__subseqs__:
			self.__subseqs__.pop(subseq)
			return True
		return False

	def __str__(self):
		return "Main Sequence: " + str(self.__mainseq__) + "\n" + "---Subsequences: " + str(self.__subseqs__) + "\n"

	def __repr__(self):
		return "Main Sequence: " + str(self.__mainseq__) + "\n" + "---Subsequences: " + str(self.__subseqs__) + "\n"

	def finalize(self):
		subseqCopy = dict(self.__subseqs__)
		for subseq in subseqCopy:
			if not self.attemptMergeRegions(subseq):
				self.removeSubseq(subseq)

	def attemptMergeRegions(self, subseq):
		if self.checkIfReshuffled(subseq):
			return False
		print subseq
		print self.__subseqs__[subseq]
		final = AlignmentInfo(sys.maxint, 0, sys.maxint, 0, 0)
		for ai in self.__subseqs__[subseq]:
			if ai.getQueryFrom()<final.getQueryFrom():
				final.setQueryFrom(ai.getQueryFrom())
			if ai.getQueryTo()>final.getQueryTo():
				final.setQueryTo(ai.getQueryTo())
			if ai.getTargetFrom()<final.getTargetFrom():
				final.setTargetFrom(ai.getTargetFrom())
			if ai.getTargetTo()>final.getTargetTo():
				final.setTargetTo(ai.getTargetTo())
			final.setEValue(ai.getEValue())
		self.__subseqs__[subseq] = [final]
		print "finalized " + str(self.getMainSeq())
		return True

	def getMatchingLength(self, subseq):
		full = set()
		print "Getting Matching Length of " + str(subseq) + " on " + str(self.getMainSeq())
		for ai in self.__subseqs__[subseq]:
			print "-----adding region " + str(ai)
			print "---------" + str(range(ai.getQueryFrom(), ai.getQueryTo()))
			full = full.union(set(range(ai.getQueryFrom(), ai.getQueryTo())))
		print "FINAL: " + str(full)
		print "FINAL LEN: " + str(len(full))
		return len(full)

	def checkIfReshuffled(self, subseq):
		print "Check if Reshuffled: " + str(subseq)
		sortedSubsegments = dict( zip( map(AlignmentInfo.getQueryFrom, list(self.__subseqs__[subseq])), list(self.__subseqs__[subseq])))
		print sortedSubsegments
		currentBottom = 0
		for bot in sortedSubsegments:
			if sortedSubsegments[bot].getTargetFrom() < currentBottom:
				print "RESHUFFLED!!!"
				return True
			else:
				currentBottom = sortedSubsegments[bot].getTargetFrom()
		return False


class ConcatFilter(SewageFilter):
	"""
	The Concatenation Filter
	The filter:
	1) Runs HMMER
	2) Parse into ConcatEvents of the appropriate type
	3) Finalize all the ConcatEvents based on the appropriate type of ConcatFilter
	4) Check all events for whether they are dirty by Concatenation of some sort (fusion or fission)
	5) Write to dirty and clean files
	"""
	__metaclass__ = ABCMeta

	def __init__(self, reference_genome, temp_directory):
		super(ConcatFilter, self).__init__()
		self.__reference_genome__ = reference_genome
		self.__clean_file__ = None
		self.__messy_file__ = None
		self.__tDir__ = temp_directory

	@abstractmethod
	def parseHmmerIntoConcatEvents(self, hmmerOutFile):
		"""
		Method should parse a HMMER output file into ConcatEvent objects of the appropriate type
		:param hmmerOutFile:
		:return:
		"""
		pass

	@abstractmethod
	def scanEvents(self, events):
		"""
		Method should scan events to determine the dirty sequences
		:param events:
		:return:
		"""
		pass


	def filter_crap(self, input_file, output_file, diagnostics_file):
		"""
		Method for filtering proteomes based on concatenation type abnormalities (i.e. fusion, fission)
		:param input_file: name of input fasta file
		:param output_file: name of output fasta file that is cleaned of extra sequences
		:param diagnostics_file: name of diagnostics file with all problematic sequences (appended to)
		:return:
		"""

		self.__clean_file__ = output_file
		self.__messy_file__ = diagnostics_file

		#parse all concat events into concat event objects
		events = [] #list of concat events

		'''
		Run HMMER
		'''

		"""use for debug
		hmmerOut = "tmp/678968.hmmerOut"
		"""
		hmmerOut = os.path.join(self.__tDir__, str(int(random.random()*1000000)) + ".hmmerOut") #make hmmerout

		hmmer_tools.loadHmmer()

		hmmer_tools.runHmmer(input_file, self.__reference_genome__, hmmerOut, self.__logfile__)
		###"""

		'''
		Parse Into Events
		'''
		#parse events
		events = self.parseHmmerIntoConcatEvents(hmmerOut)

		'''
		Finalize Events
		'''
		#finalize events
		for event in events:
			event.finalize()

		#scan events
		dirtySequences = self.scanEvents(events)

		#TODO: not sure about these 2 lines, have to test, I think these are debugging artifacts
		import sys
		print >> sys.stderr, dirtySequences


		'''
		Handle the output, dirty and clean
		'''
		#Open streams
		with FastaReader(input_file) as reader:
			with FastaWriter(output_file) as cleanWriter:
				with FastaWriter(diagnostics_file, options="a") as dirtyWriter:
					#loop over all the sequences
					nextSeq = reader.readSequence()
					while nextSeq is not FastaReader.EOF:
						#if the sequence is dirty, write to dirty
						if nextSeq in dirtySequences:
							print "Dirty: " + str(nextSeq)
							tmpDirtySeq = set()
							placeholderSeq = dirtySequences.pop()
							#loop until your the placeholder seq matches the next seq
							while placeholderSeq != nextSeq:
								tmpDirtySeq.add(placeholderSeq)
								placeholderSeq = dirtySequences.pop()
							dirtySequences = dirtySequences.union(tmpDirtySeq)
							#add note to the writer about why a sequence is bad
							nextSeq.addNote(placeholderSeq.getNotes().rstrip())
							#make sure the sequence is bad for a reason (filter bug if not)
							if placeholderSeq.getNotes() is "":
								logtools.add_fatal_error("Dirty Sequence should have notes!!!", self.__logfile__)
								raise BrokenFilterError("Dirty Sequence should have notes!!!")
							#write to dirty
							dirtyWriter.writeSequence(nextSeq)
						else:
							#Make sure clean sequence does not have a note already
							if nextSeq.getNotes() is not "":
								logtools.add_fatal_error("Clean Sequence should not have notes!!!", self.__logfile__)
								raise BrokenFilterError("Clean Sequence shouldn't have notes!!!")
							#write to clean
							cleanWriter.writeSequence(nextSeq)
						#iterate
						nextSeq = reader.readSequence()
