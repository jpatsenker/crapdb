from os.path import basename
import os

from filters.sewagefilter import SewageFilter
from filters.sewagefilter import BrokenFilterError
from file_paths import *
from aux import logtools
from aux.jobs import Job


class RedundancyFilter(SewageFilter):
    """
    The Redundancy Filter runs CD-HIT on the sequences, and filters out sequences that are redundant with eachother to some threshold, and fractional level
    We run CD-HIT with the threshold as self.__threshold_level__
    A sequence will be removed if it is above the fractional level (of the central sequence in the CD-HIT cluster), self.__fractional_level__,
    """

    __name__ = "INTERSEQUENCE_REDUNDANCY_FILTER"

    '''
    Location of CD-HIT on orchestra
    '''
    __cd_hit__ = CDHIT_PATH

    __threshold_level__ = None
    __fractional_level__ = None


    __temp_hash__ = None

    def __init__(self, thresh, frac, tempDir, lfil = None):
        super(RedundancyFilter, self).__init__()
        #main params
        self.__threshold_level__ = thresh
        self.__fractional_level__ = frac
        #needs tmp directory, log file is optional but good for debug
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
        '''
        Run CD-HIT
        '''
        # temporary file for cdhit raw output
        temporary = os.path.join(self.__tDir__, "%s.cdhit.raw" % basename(input_file))
        # print self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__)
        job = Job(self.__cd_hit__ + " -i " + input_file + " -o " + temporary +
                  " -c " + str(self.__threshold_level__) + " -d 0",lfil=self.__logfile__)
        job.run(wait=True) #submit job
        
        self.prepare_temp_hash(input_file, temporary + ".clstr")
        logtools.add_line_to_log(self.__logfile__, "---Filtering redundant sequences")

        '''
        Parse CD-HIT and filter
        '''
        #open streams
        with open(temporary + ".clstr", "r") as temp_stream:
            with open(output_file, "w") as out_stream:
                with open(diagnostics_file, "a") as d_stream:
                    #read
                    tline = temp_stream.readline()
                    #initialize
                    central_len = 0
                    central_seq = ""
                    #loop through lines in .clstr file
                    while tline:
                        #if the line is not the cluster ID
                        if tline[0] != ">":
                            with open(input_file, "r") as in_stream:
                                line = self.find_corresponding_line(tline, in_stream, rseq=True)
                            #check whether filter is necessary
                            if tline.split()[-1] == "*" or float(len(line))/float(central_len) < self.__fractional_level__:
                                #write to clean
                                with open(input_file, "r") as in_stream:
                                    out_stream.write(self.find_corresponding_line(tline, in_stream))
                            else:
                                #write to dirty
                                with open(input_file, "r") as in_stream:
                                    d_stream.write(self.find_corresponding_line(tline, in_stream, bad=" Sequence is a Redundant Fragment with Central Sequence: " + central_seq))
                        else:
                            #if it is a cluster ID
                            savpos = temp_stream.tell()
                            '''TODO code below is definitley inefficient'''
                            #get the sequence length of the cluster center
                            central_len = self.getCentralLen(temp_stream, input_file)
                            #seek back to the cluster beginning
                            temp_stream.seek(savpos)
                            #get the central sequence itself
                            central_seq = self.getCentralSeq(temp_stream)
                            #seek back to cluster beginning
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
        """
        Create a hash for the CD-HIT lines to reduce search from O(n^2) to O(n) worst case time
        :param input_file:
        :param cdhit_file:
        :return:
        """
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
        """
        Finds corresponding line to cdhit line
        :param cdhitline:
        :param in_stream:
        :param bad: string message to add to the sequence in the dirty file
        :param rseq: whether or not to return just the sequence. Otherwise full fasta_id with sequence attached
        :return:
        """

        #split id and data [parse line]
        prot = cdhitline.split()[2].rstrip(".")
        #figure out position based on hash
        try:
            position = self.__temp_hash__[prot]
        except KeyError:
            #complain about poor hashing, shouldn't happen
            #this is a bug in the CDHIT filter
            print "Improperly put together hash in CDHIT filter!!! Couldn't find start" + prot + "end"
            print "From line: " + cdhitline
            print self.__temp_hash__
            logtools.add_fatal_error(self.__logfile__, "Hash Error in Redundancy Filter. Couldn't find '" + prot + "'")
            raise BrokenFilterError(RedundancyFilter.__name__)

        #use position to find the corresponding line
        in_stream.seek(position)
        l = in_stream.readline()
        seq = in_stream.readline()

        #if only sequence required return just the sequence
        if rseq:
            return seq.rstrip("\n")

        #if bad is set to a string, add that to the fasta id line, and return the fasta id with the seq (handle all new lines)
        if bad is not None:
            l = l.rstrip("\n") + bad + "\n" + seq
        else:
            l = l + seq
        return l


    def getCentralLen(self, temp_stream, input_file):
        """
        Get the length of the central sequence of a CD-HIT cluster
        :param temp_stream: stream object as an input stream of the .clstr file
        :param input_file: input file
        :return:
        """
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
        """
        Get the central sequence of a CD-HIT cluster
        :param temp_stream:
        :return:
        """
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
