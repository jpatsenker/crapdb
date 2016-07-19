from abc import ABCMeta, abstractmethod

class SewageFilter:
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
        return self.__name__

    def set_logfile(self, logfile):
        self.__logfile__ = logfile

    def has_logfile(self):
        return self.__logfile__ is not None

class BrokenFilterError(Exception):
    def __init__(self, fil):
        super(BrokenFilterError, self).__init__("The filter <" + str(fil) + "> has broken!!!")