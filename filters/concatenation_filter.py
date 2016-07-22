from abc import ABCMeta, abstractmethod
import sys

from filters.sewagefilter import SewageFilter
from filters.sewagefilter import BrokenFilterError
from model.fasta_tools import FastaReader
from model.fasta_tools import FastaWriter
from aux import hmmer_tools
import random
from aux import logtools

class AlignmentInfo:

    def __init__(self, qf, qt, tf, tt, e):
        self.__queryFrom__ = qf
        self.__queryTo__ = qt
        self.__targetFrom__ = tf
        self.__targetTo__ = tt
        self.__evalue__ = e

    def getQueryFrom(self):
        return self.__queryFrom__
    def getQueryTo(self):
        return self.__queryTo__
    def getTargetFrom(self):
        return self.__targetFrom__
    def getTargetTo(self):
        return self.__targetTo__
    def getEValue(self):
        return self.__evalue__
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
    def __str__(self):
        return "Query: (" + str(self.__queryFrom__) + "->" + str(self.__queryTo__) + "), Target: (" + str(self.__targetFrom__) + "->" + str(self.__targetTo__) + "), e-value: " + str(self.__evalue__)
    def __repr__(self):
        return str(self)


class ConcatEvent:
    """
    Class for holding onto Fission/Fusion (fF) Events
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
        for subseq in self.__subseqs__:
            if not self.attemptMergeRegions(subseq):
                self.removeSubseq(subseq)

    def attemptMergeRegions(self, subseq):
        if self.checkIfReshuffled(subseq):
            return False
        final = AlignmentInfo(sys.maxint, 0, sys.maxint, 0, 0)
        for ai in self.__subseqs__[subseq]:
            if ai.getQueryFrom()<final.getQueryFrom():
                final.setQueryFrom(ai.getQueryFrom())
            if ai.getQueryTo()>final.getQueryTo():
                final.setQueryTo(ai.getQueryTo())
            if ai.getTargetFrom()<final.getTargetFrom():
                final.setTargetFrom(ai.getTargetFrom())
            if ai.getTargetTo()<final.getTargetTo():
                final.setTargetTo(ai.getTargetTo())
            final.setEValue(ai.getEValue())
        self.__subseqs__[subseq] = [final]
        return True

    def getMatchingLength(self, subseq):
        full = set()
        for ai in self.__subseqs__[subseq]:
            full.union(set(range(ai.getQueryFrom(), ai.getQueryTo())))
        return len(full)

    def checkIfReshuffled(self, subseq):
        sortedSubseqs = dict( zip( map(AlignmentInfo.getQueryFrom, list(self.__subseqs__[subseq])), list(self.__subseqs__[subseq])))
        currentBottom = 0
        for bot in sortedSubseqs:
            if sortedSubseqs[bot].getTargetFrom() < currentBottom:
                return True
        return False


class ConcatFilter(SewageFilter):
    __metaclass__ = ABCMeta

    def __init__(self, reference_genome):
        super(ConcatFilter, self).__init__()
        self.__reference_genome__ = reference_genome
        self.__clean_file__ = None
        self.__messy_file__ = None

    @abstractmethod
    def parseHmmerIntoConcatEvents(self, hmmerOutFile):
        pass

    @abstractmethod
    def scanEvents(self, events):
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

        """DEBUG!!!!
        hmmerOut = "test/sturgeon_frog.hmmerOut"
        """
        hmmerOut = "tmp/" + str(int(random.random()*1000000)) + ".hmmerOut" #make hmmerout

        hmmer_tools.loadHmmer()

        hmmer_tools.runHmmer(input_file, self.__reference_genome__, hmmerOut, self.__logfile__)
        ###"""

        events = self.parseHmmerIntoConcatEvents(hmmerOut)

        #finalize events
        for event in events:
            event.finalize()

        dirtySequences = self.scanEvents(events)

        import sys
        print >> sys.stderr, dirtySequences

        with FastaReader(input_file) as reader:
            with FastaWriter(output_file) as cleanWriter:
                with FastaWriter(diagnostics_file, options="a") as dirtyWriter:
                    nextSeq = reader.readSequence()
                    while nextSeq is not FastaReader.EOF:
                        if nextSeq in dirtySequences:
                            print "Dirty: " + str(nextSeq)
                            tmpDirtySeq = set()
                            placeholderSeq = dirtySequences.pop()
                            while placeholderSeq != nextSeq:
                                #print placeholderSeq
                                #print dirtySequences
                                tmpDirtySeq.add(placeholderSeq)
                                placeholderSeq = dirtySequences.pop()
                            dirtySequences = dirtySequences.union(tmpDirtySeq)
                            #print dirtySequences
                            nextSeq.addNote(placeholderSeq.getNotes().rstrip())
                            if placeholderSeq.getNotes() is "":
                                logtools.add_fatal_error("Dirty Sequence should have notes!!!", self.__logfile__)
                                raise BrokenFilterError("Dirty Sequence should have notes!!!")
                            dirtyWriter.writeSequence(nextSeq)
                        else:
                            #print "Clean: " + str(nextSeq)
                            if nextSeq.getNotes() is not "":
                                logtools.add_fatal_error("Clean Sequence should not have notes!!!", self.__logfile__)
                                raise BrokenFilterError("Clean Sequence shouldn't have notes!!!")
                            cleanWriter.writeSequence(nextSeq)
                        nextSeq = reader.readSequence()
