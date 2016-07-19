from os.path import basename
import os

from filters.sewagefilter import SewageFilter
from aux import lsftools as lsf


class FastaCheckerFilter(SewageFilter):

    __name__ = "FASTA_CHECK_FILTER"

    __fasta_checker__ = "/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker_for_crap.pl"

    def __init__(self):
        super(FastaCheckerFilter, self).__init__()

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run fasta checker on input file and strip of redundant sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """
        temporary = "tmp/" + basename(input_file) + ".raw"
        open(temporary, "w").close()
        temporary_errors = "tmp/" + basename(input_file) + ".errors"
        lsf.run_job('"perl ' + self.__fasta_checker__ + " " + input_file + " 0 2>" + temporary_errors + " > " + temporary + '"', bsub_output="tmp/test.out", wait=True, dont_clean=True, lfil = self.__logfile__) #submit lsf job
        # with open(temporary_errors, "r") as tempErrors:
        #     if len(tempErrors.read()) > 0:
        #         SewageFilter.break_filter() #incase of errors break filter, cause system to halt with improper format errors
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
                                diag_stream.write(line.rstrip("\n") + " Sequence Discarded by Fasta Checker\n" + sequence)
                        else:
                            cline = mark_stream.readline()
                        line = in_stream.readline()
                    else:
                        cline = mark_stream.readline()
                        line = in_stream.readline()