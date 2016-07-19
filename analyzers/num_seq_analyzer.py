from analyzers.sewageanalyzer import SewageAnalyzer
from aux import logtools


class NumSeqAnalyzer(SewageAnalyzer):

    __name__ = "NUMBER_SEQUENCES_ANALYZER"

    __log_fil__ = None
    __mess_fil__ = None



    def __init__(self, lfil = None, mfil = None):
        super(SewageAnalyzer, self).__init__()
        self.__log_fil__ = lfil
        self.__mess_fil__ = mfil

    def analyze_crap(self, input_file, analysis_file, graphic=False):
        with open(input_file, "r") as input_stream:
            every = input_stream.read()
            stuff = every.split("\n")
            num_seq = int(len(stuff)/2)
        with open(analysis_file, "w") as analysis_stream:
            analysis_stream.write(str(num_seq))
        if self.__log_fil__ is not None:
            logtools.add_line_to_log(self.__log_fil__, "Number of non-CRAP sequences left: " + str(num_seq))
        if self.__mess_fil__ is not None:
            with open(self.__mess_fil__, "r") as input_stream:
                every = input_stream.read()
                stuff = every.split("\n")
                mess_seq = int(len(stuff)/2)
            logtools.add_line_to_log(self.__log_fil__, "Number of CRAP sequences currently: " + str(mess_seq))