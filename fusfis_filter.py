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

class FusionFissionFilter(SewageFilter):

    __name__ = "Ff_CHECK_FILTER"

    __cd_hit__ = "/opt/cdhit-4.6/cd-hit"
    __filt_human_genome__ = "filtered_human_non_redundant.cdhit"


    __threshold_level__ = None
    __fractional_length__ = None

    def __init__(self, thresh, frac):
        super(SewageFilter, self).__init__()
        self.__threshold_level__ = thresh
        self.__fractional_length__ = frac

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run cdhit on input file concatenated with human genome and strip of redundant sequences, testing for fusion/fission of other possible genes
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """

        #concatenate files into string, every sequence id in human genome starts with ">HUMAN_CRAP" tag
        with open(input_file, "r") as in_stream:
            everything = in_stream.read().rstrip("\n") + "\n"
            with open(self.__filt_human_genome__, "r") as h_stream:
                everything += h_stream.read().replace(">", ">HUMAN_CRAP")

        temp_input = "tmp/" + basename(input_file) + ".Ffinput"
        with open(temp_input, "w") as t_stream:
            t_stream.write(everything)
        open(output_file, "w").close() #open and close out file so that it is blank

        temporary = "tmp/" + basename(input_file) + ".cdhit.raw" #temporary file for cdhit raw output
        #print self.__cd_hit__ + " -i " + input_file + " -o " + temporary + " -c " + str(self.__threshold_level__)
        lsf.run_job(self.__cd_hit__ + " -i " + temp_input + " -o " + temporary + " -c " + str(self.__threshold_level__), wait=True) #submit lsf job
        with open(temporary + ".clstr", "r") as temp_stream:
            tline = temp_stream.readline()
            while tline:
                cluster = ""
                tline = temp_stream.readline()
                while tline and tline[0] != ">":
                    cluster += tline
                    tline = temp_stream.readline()
                important_cluster = False
                cluster_seqs = cluster.rstrip("\n").split("\n")
                cluster_lines = []
                for seq in cluster_seqs:
                    with open(temp_input, "r") as in_stream:
                        cluster_lines.append(find_corresponding_line(seq, in_stream))
                for line in cluster_lines:
                    assert line[0] == ">"
                    if line[:11] == ">HUMAN_CRAP":
                        important_cluster = True
                if important_cluster:
                    for i in range(len(cluster_lines)):
                        if cluster_lines[i][:11] != ">HUMAN_CRAP":
                            if cluster_seqs[i].split()[-1] == "*":
                                human_len = 0
                                for line in cluster_seqs:
                                    if line.split()[2][:11] == ">HUMAN_CRAP":
                                        human_len = int(line.split()[1].rstrip(",").rstrip("a"))
                                        #print line
                                #print cluster_seqs[i] + " " + str(float(len(cluster_lines[i].split("\n")[1]))/human_len)
                                #print float(len(cluster_lines[i].split("\n")[1]))
                                #print human_len
                                if float(len(cluster_lines[i].split("\n")[1]))/human_len > (2-self.__fractional_length__):
                                    with open(diagnostics_file, "a") as dstream:
                                        dstream.write(cluster_lines[i].split("\n")[0] + " Sequence is Fusion Fragment\n" + cluster_lines[i].split("\n")[1] + "\n")
                                else:
                                    with open(output_file, "a") as ostream:
                                        ostream.write(cluster_lines[i])
                            else:
                                human_len = 0
                                for line in cluster_seqs:
                                    if line.split()[2][:11] == ">HUMAN_CRAP":
                                        human_len = int(line.split()[1].rstrip(",").rstrip("a"))
                                if float(len(cluster_lines[i].split("\n")[1]))/human_len < self.__fractional_length__:
                                    with open(diagnostics_file, "a") as dstream:
                                        dstream.write(cluster_lines[i].split("\n")[0] + " Sequence is Fission Fragment\n" + cluster_lines[i].split("\n")[1] + "\n")
                                else:
                                    with open(output_file, "a") as ostream:
                                        ostream.write(cluster_lines[i])
                else:
                    for line in cluster_lines:
                        if line[:11] != ">HUMAN_CRAP":
                            with open(output_file, "a") as ostream:
                                ostream.write(line)