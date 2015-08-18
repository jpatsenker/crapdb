from os.path import basename
from sewagefilter import SewageFilter
import lsftools as lsf


def find_corresponding_line(cdhitline, in_stream, bad=None):
    l = in_stream.readline()
    while l:
        prot = cdhitline.split()[3].rstrip(".")
        r = len(prot)
        if prot == l[:r]:
            seq = in_stream.readline()
            if bad is not None:
                l = l.rstrip("\n") + bad + seq
            else:
                l = l + seq
            return l
        l = in_stream.readline()


class RedundancyFilter(SewageFilter):

    __name__ = "CDHIT_CHECK_FILTER"

    __cd_hit__ = "/opt/cdhit-4.6/cd-hit"

    __threshold_level__ = None
    __fractional_level__ = None

    def __init__(self, thresh, frac):
        super(SewageFilter, self).__init__()
        self.__threshold_level__ = thresh
        self.__fractional_level__ = frac

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run cdhit on input file and strip of redundant sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """
        open(output_file, "w").close() #open and close out file so that it is blank

        temporary = "tmp/" + basename(input_file) + ".cdhit.raw" #temporary file for cdhit raw output
        print self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__)
        lsf.run_job(self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__)) #submit lsf job
        with open(temporary + ".clstr", "r") as temp_stream:
            with open(input_file, "r") as in_stream:
                tline = temp_stream.readline()
                while tline:
                    if tline[0] != ">":
                        if tline.split()[-1] == "*" or float(tline.split()[-1].rstrip("%")) > self.__fractional_level__:
                            with open(output_file, "a") as out_stream:
                                out_stream.write(find_corresponding_line(tline, in_stream))
                        else:
                            with open(diagnostics_file, "a") as d_stream:
                                d_stream.write(find_corresponding_line(tline, in_stream, bad="Sequence caught in redundancy filter"))
                    tline = temp_stream.readline()