from abc import ABCMeta, abstractmethod
from sewagefilter import SewageFilter
from fasta_tools import FastaReader
from fasta_tools import FastaWriter
from fasta_tools import Sequence
import hmmer_tools
from hmmer_tools import DomTableRow
from hmmer_tools import DomTableReader
import random




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
            self.__subseqs__[subseq] = 0

    def setCoords(self, subseq, coordinate):
        """
        Method for setting coordinates of sequence
        """
        if self.__subseqs__.has_key(subseq):
            self.__subseqs__[subseq] = coordinate
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

    def getMatchingLength(self, subseq):
        return self.__subseqs__[subseq][1]-self.__subseqs__[subseq][0]

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

        ###DEBUG!!!!
        hmmerOut = "test/sturgeon_frog.hmmerOut"
        ###

        """
        hmmerOut = "tmp/" + str(int(random.random()*1000000)) + ".hmmerOut" #make hmmerout

        hmmer_tools.loadHmmer()

        hmmer_tools.runHmmer(input_file, self.__reference_genome__, hmmerOut)
        """

        events = self.parseHmmerIntoConcatEvents(hmmerOut)

        dirtySequences = self.scanEvents(events)

        import sys
        print >> sys.stderr, dirtySequences

        with FastaReader(input_file) as reader:
            with FastaWriter(output_file) as cleanWriter:
                with FastaWriter(diagnostics_file) as dirtyWriter:
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
                                raise Exception("Dirty Sequence should have notes!!!")
                            dirtyWriter.writeSequence(nextSeq)
                        else:
                            print "Clean: " + str(nextSeq)
                            if nextSeq.getNotes() is not "":
                                raise Exception("Clean Sequence shouldn't have notes!!!")
                            cleanWriter.writeSequence(nextSeq)
                        nextSeq = reader.readSequence()
