from os.path import basename
from sewagefilter import SewageFilter
import lsftools as lsf


def find_corresponding_line(cdhitline, in_stream, bad=None, rseq = False):
    l = in_stream.readline()
    while l:
        prot = cdhitline.split()[2].rstrip(".")
        r = len(prot)
        if prot == l[:r]:
            #print "Found " + prot
            #print prot + "\n"
            #print l[:r] + "\n"
            seq = in_stream.readline()
            if rseq:
                return seq.rstrip("\n")
            if bad is not None:
                l = l.rstrip("\n") + bad + "\n" + seq
            else:
                l = l + seq
            return l
        l = in_stream.readline()
    #print cdhitline + "\n"
    assert 1 == 0


def getCentralLen(temp_stream, input_file):
    l = ""
    n = temp_stream.readline()
    while n and n[0] != ">":
        l += n
        n = temp_stream.readline()
    #print "Cluster: " + l
    linfo = l.split("\n")
    for line in linfo:
        if line.split()[-1]=="*":
            with open(input_file, "r") as in_stream:
                return len(find_corresponding_line(line, in_stream, rseq=True))

class RedundancyFilter(SewageFilter):

    __name__ = "CDHIT_CHECK_FILTER"

    __cd_hit__ = "/opt/cdhit-4.6/cd-hit"

    __threshold_level__ = None
    __fractional_level__ = None
    __log_file__ = None

    def __init__(self, thresh, frac, lfil = None):
        super(SewageFilter, self).__init__()
        self.__threshold_level__ = thresh
        self.__fractional_level__ = frac
        self.__log_file__ = lfil

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run cdhit on input file and strip of redundant sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """

        temporary = "tmp/" + basename(input_file) + ".cdhit.raw" #temporary file for cdhit raw output
        #print self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__)
        lsf.run_job(self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__), wait=True, lfil=self.__log_file__) #submit lsf job
        with open(temporary + ".clstr", "r") as temp_stream:
            with open(output_file, "w") as out_stream:
                with open(diagnostics_file, "a") as d_stream:
                    tline = temp_stream.readline()
                    central_len = 0
                    while tline:
                        if tline[0] != ">":
                            with open(input_file, "r") as in_stream:
                                line = find_corresponding_line(tline, in_stream, rseq=True)
                            if tline.split()[-1] == "*" or len(line)/central_len > self.__fractional_level__:
                                #print "this one is ok: " + tline
                                with open(input_file, "r") as in_stream:
                                    out_stream.write(find_corresponding_line(tline, in_stream))
                            else:
                                with open(input_file, "r") as in_stream:
                                    d_stream.write(find_corresponding_line(tline, in_stream, bad=" Sequence Is Redundant Fragment"))
                        else:
                            savpos = temp_stream.tell()
                            #print str(savpos)
                            central_len = getCentralLen(temp_stream, input_file)
                            #print "central len: " + str(central_len)
                            temp_stream.seek(savpos)
                            #print "seeking back to " + str(savpos)
                        tline = temp_stream.readline()
                        #print tline