from concatenation_filter import ConcatFilter
from concatenation_filter import ConcatEvent
from fasta_tools import Sequence

class FusionEvent(ConcatEvent):
	def getScore():
		return 0


class FusionFilter(ConcatFilter):

	def parseHmmerIntoConcatEvents(self, hmmerOutFile):
		events = {}
	    with DomTableReader(hmmerOutFile) as reader:
	        row = reader.readRow()
	        while not row == DomTableReader.EOF:
	            if row == DomTableReader.BADFORMAT:
	                break
	            try:
	            	events[Sequence(row.getQuery(), Sequence.PLACEHOLDER)].addSubseq(Sequence(row.getTarget(), Sequence.PLACEHOLDER))
	            	events[Sequence(row.getQuery(), Sequence.PLACEHOLDER)].setCoords(Sequence(row.getTarget(), Sequence.PLACEHOLDER), (row.getQueryFrom(), row.getQueryTo()))
	            except KeyError as e:
	            	events[Sequence(row.getQuery(), Sequence.PLACEHOLDER)] = FusionEvent(Sequence(row.getTarget(), Sequence.PLACEHOLDER))
	            	events[Sequence(row.getQuery(), Sequence.PLACEHOLDER)].addSubseq(Sequence(row.getTarget(), Sequence.PLACEHOLDER))
	            	events[Sequence(row.getQuery(), Sequence.PLACEHOLDER)].setCoords(Sequence(row.getTarget(), Sequence.PLACEHOLDER), (row.getQueryFrom(), row.getQueryTo()))
	            row = reader.readRow()
	    return events.values()