from concatenation_filter import ConcatFilter
from concatenation_filter import ConcatEvent
from hmmer_tools import DomTableReader
from fasta_tools import Sequence


EXON_LENGTH = 30


class FissionEvent(ConcatEvent):

	def __init__(self, mainseq):
		super(FissionEvent, self).__init__(mainseq)

	def getScore():
		return 0

class FissionFilter(ConcatFilter):

	def __init__(self, reference_genome):
		super(FissionFilter, self).__init__(reference_genome)

	def parseHmmerIntoConcatEvents(self, hmmerOutFile):
		events = {}
		with DomTableReader(hmmerOutFile) as reader:
			row = reader.readRow()
			while not row == DomTableReader.EOF:
				if row == DomTableReader.BADFORMAT:
					break
				seq = Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen()))
				ss = Sequence(row.getQuery(), Sequence.PLACEHOLDER(row.getQLen()))
				try:
					events[seq].addSubseq(ss)
					events[seq].setCoords(ss, (int(row.getTargetFrom()), int(row.getTargetTo())))
				except KeyError as e:
					#print e
					#print "Making new event for sequence, " + str(seq) + " (Hash: " + str(hash(seq)) + ")"
					#print events
					events[seq] = FissionEvent(seq)
					events[seq].addSubseq(ss)
					events[seq].setCoords(ss, (int(row.getTargetFrom()), int(row.getTargetTo())))
				row = reader.readRow()
		return events.values()

	def checkSuitability(self, sequenceCoords, candidateCoords):
		"""
		Checks Suitability of Fission candidate, requiring overlap of less than 1 exon
		"""
		s = range(sequenceCoords[0], sequenceCoords[1])
		c = range(candidateCoords[0], candidateCoords[1])
		ss = set(s)
		i = ss.intersection(c)
		return len(i) < EXON_LENGTH


	def mark(self, seq, pair, ref):
		print "seq: " + str(seq)
		print "pair " + str(pair)
		print "ref " + str(ref)
		seq.addNote("Sequence is Fission of " + ref.getIdentity() + " with sequence " + seq.getIdentity())

	def scanEvents(self, events):
		#create temporary dictionary
		new_events = dict( zip( map(ConcatEvent.getMainSeq, list(events)), list(events) ) )

		print events

		print new_events

		needClean = True
		while needClean:
			needClean = False

			#filter set of events that aren't real events
			for event in events:
				subseqs = event.getSubseqs()
				if len(subseqs) == 0 or len(subseqs) == 1:
					if event.getMainSeq() in new_events:
						new_events.pop(event.getMainSeq())
				else:
					for subseq in subseqs.keys():
						#if it isn't a realistic match, (< Exon length)
						#OR
						#if it is a match of the same length
						if event.getMatchingLength(subseq) > event.getMainSeq().getSequenceLength() - EXON_LENGTH or event.getMatchingLength(subseq) < EXON_LENGTH:
							print event
							print subseq
							for e in new_events.values():
								e.removeSubseq(subseq)
							needClean = True
			events = list(new_events.values())


		dirtySequences = []
		#mark every query gene for fission if a suitable partner is found
		for event in events:
			subseqs = event.getSubseqs()
			for subseq in subseqs.keys():
				for candidate in subseqs.keys():
					if self.checkSuitability(subseqs[subseq], subseqs[candidate]):
						self.mark(subseq, candidate, event.getMainSeq())
						dirtySequences.append(subseq)

		return set(dirtySequences)