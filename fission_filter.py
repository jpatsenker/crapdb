from concatenation_filter import ConcatFilter
from concatenation_filter import ConcatEvent


EXON_LENGTH = 30


class FissionEvent(ConcatEvent):
	
	def __init__(self, mainseq):
		super(ConcatEvent, self).__init__(mainseq)

	def getScore():
		return 0

class FissionFilter(ConcatFilter):
	
	def __init__(self, reference_genome):
        super(ConcatFilter, self).__init__(reference_genome)

	def parseHmmerIntoConcatEvents(self, hmmerOutFile):
		events = {}
		with DomTableReader(hmmerOutFile) as reader:
	    	row = reader.readRow()
	    	while not row == DomTableReader.EOF:
	    		if row == DomTableReader.BADFORMAT:
					break
				try:
	            	events[Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen()))].addSubseq(Sequence(row.getQuery(), Sequence.PLACEHOLDER(row.getQLen())))
	            	events[Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen()))].setCoords(Sequence(row.getQuery(), Sequence.PLACEHOLDER(row.getQLen())), (row.getTargetFrom(), row.getTargetTo()))
	            except KeyError as e:
	            	events[Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen()))] = FissionEvent(Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen())))
	            	events[Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen()))].addSubseq(Sequence(row.getQuery(), Sequence.PLACEHOLDER(row.getQLen())))
					events[Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen()))].setCoords(Sequence(row.getQuery(), Sequence.PLACEHOLDER(row.getQLen())), (row.getTargetFrom(), row.getTargetTo()))
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


	def mark(seq, pair, ref):
		seq.addNote("Sequence is Fission of " + ref.getIdentity() + " with sequence " + seq.getIdentity())

	def scanEvents(self, events):
		#create temporary dictionary
		new_events = zip( map(ConcatEvent.getMainSequence, list(events)), list(events) )

		needClean = True
		while needClean:
			needClean = False

			#filter set of events that aren't real events
			for event in events:
	            subseqs = event.getSubseqs()
	            if len(subseqs) == 0 or len(subseqs) == 1:
	            	new_events.pop(event.getMainSeq())
	            else:
	            	for subseq in subseqs.keys():
	            		#if it isn't a realistic match, <Exon length
	            		if event.getMatchingLength(subseq) < EXON_LENGTH:
	            			new_events.pop(event.getMainSeq())
	            			needClean = True
	            		#if it is a match of the same length
	            		if event.getMatchingLength(subseq) > event.getMainSeq().getSequenceLength() - EXON_LENGTH:
	            			for e in new_events:
	            				if subseqs[subseq] in e.getSubseqs()
	            					e.removeSubseq(subseqs[subseq])
	            			needClean = True
	        events = list(new_events)


	    dirtySequences = []
	    #mark every query gene for fission if a suitable partner is found
	    for event in events:
	    	subseqs = event.getSubseqs()
	    	for subseq in subseqs.keys():
	    		for candidate in subseqs.keys():
	    			if self.checkSuitability(subseqs[subseq], subseqs[candidate]):
	    				mark(subseq, candidate, event.getMainSeq())
	    				dirtySequences.append(subseq)

	    return dirtySequences