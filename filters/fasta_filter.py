from os.path import basename
import os

from filters.sewagefilter import SewageFilter
from file_paths import *
from aux.jobs import Job


class FastaCheckerFilter(SewageFilter):
    """
    This is a filter for fasta errors. This script runs the fasta checker and
    """

    __name__ = "FASTA_CHECK_FILTER"

    #location of the fasta checker script
    __fasta_checker__ = FASTACHECKER_PATH
    
    def __init__(self, tempDir):
        super(FastaCheckerFilter, self).__init__()
        #needs location of the temporary directory for fasta checker output
        self.__tDir__ = tempDir

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run fasta checker on input file and strip of redundant sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """
        '''
        Run fasta checker
        '''
        temporary = self.__tDir__ + basename(input_file) + ".raw" #create out file
        open(temporary, "w").close() #wipe file if exists
        temporary_errors = self.__tDir__ + basename(input_file) + ".errors" #create error out file
        job = Job(PERL_PATH + " " + self.__fasta_checker__ + " " + input_file + " 0 2>" + temporary_errors + " > " + temporary, lfil = self.__logfile__)
        job.run(output=self.__tDir__ + "test.out", wait=True) #submit job
        '''
        Parse output of fasta checker
        '''
        #the temporary out is already a clean fasta file
        os.rename(temporary, output_file)

        '''
        find if dirty sequences exist and put them into dirty file
        '''
        #open streams
        with open(input_file, "r") as in_stream:
            with open(output_file, "r") as good_seq_stream:
                line = in_stream.readline()
                cline = good_seq_stream.readline()
                while line:
                    #if on sequence line keep going, else check if that exists in the temp file
                    if line[0] == ">":
                        #if the lines don't match up, read sequence from input stream and write to dirty
                        #else, keep reading from both streams
                        if line != cline:
                            sequence = in_stream.readline()
                            with open(diagnostics_file, "a") as diag_stream:
                                print line[0:50], "is not", cline[0:50]
                                diag_stream.write(line.rstrip("\n") + " Sequence Discarded by Fasta Checker\n" + sequence)
                        else:
                            cline = good_seq_stream.readline()
                        line = in_stream.readline()
                    else:
                        #continue
                        cline = good_seq_stream.readline()
                        line = in_stream.readline()