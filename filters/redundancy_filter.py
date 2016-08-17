from os.path import basename

from filters.sewagefilter import SewageFilter
from filters.sewagefilter import BrokenFilterError
from aux import lsftools as lsf, logtools


class RedundancyFilter(SewageFilter):

    __name__ = "INTERSEQUENCE_REDUNDANCY_FILTER"

    __cd_hit__ = "/opt/cdhit-4.6/cd-hit"

    __threshold_level__ = None
    __fractional_level__ = None


    __temp_hash__ = None

    def __init__(self, thresh, frac, tempDir, lfil = None):
        super(RedundancyFilter, self).__init__()
        self.__threshold_level__ = thresh
        self.__fractional_level__ = frac
        self.__logfile__ = lfil
        self.__tDir__= tempDir

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run cdhit on input file and strip of redundant sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """

        temporary = self.__tDir__ + basename(input_file) + ".cdhit.raw" #temporary file for cdhit raw output
        #print self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__)
        lsf.run_job(self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__) + " -d 0", wait=True, lfil=self.__logfile__) #submit lsf job
        self.prepare_temp_hash(input_file, temporary + ".clstr")
        logtools.add_line_to_log(self.__logfile__, "---Filtering redundant sequences")
        with open(temporary + ".clstr", "r") as temp_stream:
            with open(output_file, "w") as out_stream:
                with open(diagnostics_file, "a") as d_stream:
                    tline = temp_stream.readline()
                    central_len = 0
                    central_seq = ""
                    while tline:
                        if tline[0] != ">":
                            with open(input_file, "r") as in_stream:
                                line = self.find_corresponding_line(tline, in_stream, rseq=True)
                            #print float(len(line))/float(central_len)
                            if tline.split()[-1] == "*" or float(len(line))/float(central_len) < self.__fractional_level__:
                                #print "this one is ok: " + tline
                                with open(input_file, "r") as in_stream:
                                    out_stream.write(self.find_corresponding_line(tline, in_stream))
                            else:
                                with open(input_file, "r") as in_stream:
                                    d_stream.write(self.find_corresponding_line(tline, in_stream, bad=" Sequence is a Redundant Fragment with Central Sequence: " + central_seq))
                        else:
                            savpos = temp_stream.tell()
                            #print str(savpos)
                            central_len = self.getCentralLen(temp_stream, input_file)
                            #print "central len: " + str(central_len)
                            temp_stream.seek(savpos)
                            central_seq = self.getCentralSeq(temp_stream)
                            temp_stream.seek(savpos)
                            #print "seeking back to " + str(savpos)
                        tline = temp_stream.readline()
                        #print tline
        logtools.add_line_to_log(self.__logfile__, "---Filtering Complete")


    def getCdhitfileIDLength(self, cdhit_file):
        #print cdhit_file
        length = 0
        with open(cdhit_file, "r") as cd_stream:
            l = cd_stream.readline()
            while l:
                if l[0] != ">":
                    if len(l.split()[2].rstrip(".")) > length:
                        length = len(l.split()[2].rstrip("."))
                l = cd_stream.readline()
        if length == 0:
            print "No proper cdhit file present: " + cdhit_file
            logtools.add_fatal_error(self.__logfile__, "No proper cdhit file found!!! Expected: " + cdhit_file)
            raise BrokenFilterError(RedundancyFilter.__name__)
        return length


    def prepare_temp_hash(self, input_file, cdhit_file):
        logtools.add_line_to_log(self.__logfile__, "---Preparing Temporary Hash of CDHIT raw output")
        r = self.getCdhitfileIDLength(cdhit_file)
        self.__temp_hash__ = {}
        with open(input_file, "r") as in_stream:
            l = in_stream.readline()
            while l:
                self.__temp_hash__[l[:r].split()[0]]=in_stream.tell()-len(l)
                in_stream.readline()
                l = in_stream.readline()
        logtools.add_line_to_log(self.__logfile__, "---Completed Temporary Hash")


    def find_corresponding_line(self, cdhitline, in_stream, bad=None, rseq = False):
        prot = cdhitline.split()[2].rstrip(".")
        try:
            position = self.__temp_hash__[prot]
        except KeyError:
            print "Improperly put together hash in CDHIT filter!!! Couldn't find start" + prot + "end"
            print "From line: " + cdhitline
            print self.__temp_hash__
            logtools.add_fatal_error(self.__logfile__, "Hash Error in Redundancy Filter. Couldn't find '" + prot + "'")
            raise BrokenFilterError(RedundancyFilter.__name__)
        in_stream.seek(position)
        l = in_stream.readline()
        seq = in_stream.readline()
        if rseq:
            return seq.rstrip("\n")
        if bad is not None:
            l = l.rstrip("\n") + bad + "\n" + seq
        else:
            l = l + seq
        return l


    def getCentralLen(self, temp_stream, input_file):
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
                    return len(self.find_corresponding_line(line, in_stream, rseq=True))

    def getCentralSeq(self, temp_stream):
        l = ""
        n = temp_stream.readline()
        while n and n[0] != ">":
            l += n
            n = temp_stream.readline()
        #print "Cluster: " + l
        linfo = l.split("\n")
        for line in linfo:
            if line.split()[-1]=="*":
                return line.split()[2].rstrip(".").lstrip(">")