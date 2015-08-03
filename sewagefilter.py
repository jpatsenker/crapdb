from abc import ABCMeta, abstractmethod

class SewageFilter:
    __metaclass__ = ABCMeta

    __name__ = None

    def __init__(self):
        super(SewageFilter, self).__init__()



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