from abc import ABCMeta, abstractmethod
from sewagefilter import SewageFilter
from fasta_tools import FastaReader
from fasta_tools import FastaWriter
from fasta_tools import Sequence
import hmmer_tools
from hmmer_tools import DomTableRow
from hmmer_tools import DomTableReader




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
            raise Exception("Cannot set coordinates for non-existant subsequence" + str(subseq) + " (main sequence: " + str(self.__mainseq__) + ")")

    def getCoords(self, subseq):
        """
        Method for getting coordinates of subsequence
        """
        try:
            return self.__subseqs__[subseq]
        except KeyError:
            raise Exception("Cannot get coordinates for non-existant subsequence" + str(subseq) + " (main sequence: " + str(self.__mainseq__) + ")")

    def getSubseqs(self):
        return list(self.__subseqs__)

    def getMainSeq(self):
        return self.__mainseq__

    def removeSubseq(self, subseq):
        self.__subseqs__.pop(subseq)

    def __string__(self):
        return "Main Sequence: " + str(self.__mainseq__) + "\n" + "Subsequences: " + str(self.__subseqs__)

    def getOverlap(self, subseq1, subseq2):
        coords1 = self.getCoords(subseq1)
        coords2 = self.getCoords(subseq2)



class ConcatFilter(SewageFilter):
    __metaclass__ = ABCMeta

     __reference_genome__ = None


    def __init__(self, reference_genome):
        super(SewageFilter, self).__init__()
        self.__reference_genome__ = reference_genome

    @abstractmethod
    def parseHmmerIntoConcatEvents(self, hmmerOutFile):
        pass

    @abstractmethod
    def output_concat_event(self, event):
        pass

    @abstractmethod
    def fixEvents(self, events):
        pass


    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Method for filtering proteomes based on concatenation type abnormalities (i.e. fusion, fission)
        :param input_file: name of input fasta file
        :param output_file: name of output fasta file that is cleaned of extra sequences
        :param diagnostics_file: name of diagnostics file with all problematic sequences (appended to)
        :return: 
        """

        #parse all concat events into concat event objects
        events = [] #list of concat events

        hmmerOut = "" #make hmmerout

        hmmer_tools.loadHmmer()
        
        hmmer_tools.runHmmer(input_file, self.__reference_genome__, hmmerOut)

        events = self.parseHmmerIntoConcatEvents(hmmerOut)

        events = self.filterEvents(events)
            














