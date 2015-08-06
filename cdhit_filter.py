from os.path import basename
import os
from sewagefilter import SewageFilter
import lsftools as lsf


class ComplexityFilter(SewageFilter):

    __name__ = "CDHIT_CHECK_FILTER"

    __cd_hit__ = "/opt/cd-hit/bin/cd-hit"

    __threshold_level__ = None

    def __init__(self, thresh):
        super(SewageFilter, self).__init__()
        self.__threshold_level__ = thresh

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run cdhit on input file and strip of redundant sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """
        temporary = "tmp/" + basename(input_file) + ".cdhit.raw" #temporary file for cdhit raw output
        lsf.run_job("python " + self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + self.__threshold_level__) #submit lsf job
        os.rename(temporary, output_file)
        with open(input_file, "r") as in_stream:
            with open(output_file, "r") as mark_stream:
                line = in_stream.readline()
                cline = mark_stream.readline()
                while line:
                    if line[0] == ">":
                        if line != cline:
                            sequence = in_stream.readline()
                            with open(diagnostics_file, "a") as diag_stream:
                                diag_stream.write(line.rstrip("\n") + " Sequence is Redundant\n" + sequence)
                        else:
                            cline = mark_stream.readline()
                        line = in_stream.readline()
                    else:
                        cline = mark_stream.readline()
                        line = in_stream.readline()