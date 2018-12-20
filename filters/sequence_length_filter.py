from filters.sewagefilter import SewageFilter
from filters.sewagefilter import BrokenFilterError
from aux import logtools


class SeqLengthFilter(SewageFilter):
    """
    Filter sequence by length. If a sequence is longer than self.__upper_thresh__ send to dirty, and if it is shorter than self.__lower_thresh__ send to dirty. Else send to clean
    """

    __name__ = "LENGTH_DISTRIBUTION_FILTER"

    __lower_thresh__ = None #smallest protein
    __upper_thresh__ = None #longest protein

    ERROR = -666

    def __init__(self, lthresh, uthresh):
        super(SeqLengthFilter, self).__init__()
        self.__lower_thresh__ = lthresh
        self.__upper_thresh__ = uthresh


    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Filter the sequences based on their length
        :param input_file:
        :param output_file:
        :param diagnostics_file:
        :return:
        """
        #make sure output is blank, and openable
        open(output_file, "w").close()

        #open input stream
        with open(input_file, "r") as input_stream:
            line = input_stream.readline()
            while line:
                #make sure line starts with >, this should always fall on a fasta id line
                try:
                    assert line[0] == ">"
                except AssertionError:
                    print line
                    logtools.add_fatal_error(self.__logfile__, "The input fasta file to this filter has invalid formatting, error on line: " + line)
                    raise BrokenFilterError(SeqLengthFilter.__name__)
                #get the sequence
                sequence = input_stream.readline()
                sequence = sequence.rstrip("\n")
                #simple check for length above an upper threshold or below a lower threshold
                if len(sequence) > self.__upper_thresh__:
                    #write to dirty
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Sequence Too Long: Length = " + str(len(sequence)) + "\n" + sequence + "\n")
                elif len(sequence) < self.__lower_thresh__:
                    #write to dirty
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Sequence Too Short: Length = " + str(len(sequence)) + "\n" + sequence + "\n")
                else:
                    #write to clean
                    with open(output_file, "a") as out_stream:
                        out_stream.write(line + sequence + "\n")
                #iterate
                line = input_stream.readline()