from sewagefilter import SewageFilter


class SeqLengthFilter(SewageFilter):

    __name__ = "LENGTH_DISTRIBUTION_FILTER"

    __lower_thresh__ = None #smallest protein
    __upper_thresh__ = None #longest protein

    def __init__(self, lthresh, uthresh):
        super(SewageFilter, self).__init__()
        self.__lower_thresh__ = lthresh
        self.__upper_thresh__ = uthresh


    def filter_crap(self, input_file, output_file, diagnostics_file):
        open(output_file, "w").close()
        with open(input_file, "r") as input_stream:
            line = input_stream.readline()
            while line:
                try:
                    assert line[0] == ">"
                except AssertionError:
                    print line
                    exit(1)
                sequence = input_stream.readline()
                sequence = sequence.rstrip("\n")
                if len(sequence) > self.__upper_thresh__:
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Sequence Too Long: Length = " + str(len(sequence)) + "\n" + sequence + "\n")
                elif len(sequence) < self.__lower_thresh__:
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Sequence Too Short: Length = " + str(len(sequence)) + "\n" + sequence + "\n")
                else:
                    with open(output_file, "a") as out_stream:
                        out_stream.write(line + sequence + "\n")
                line = input_stream.readline()