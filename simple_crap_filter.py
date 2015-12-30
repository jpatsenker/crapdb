from sewagefilter import SewageFilter


class SimpleFilter(SewageFilter):

    __name__ = "SIMPLE_CRAP_FILTER"

    __ms__ = None
    __xs__ = None


    def __init__(self, ms, xs):
        super(SewageFilter, self).__init__()
        self.__ms__=ms
        self.__xs__=xs

    def filter_crap(self, input_file, output_file, diagnostics_file):
        open(output_file, "w").close()
        with open(input_file, "r") as input_stream:
            line = input_stream.readline()
            while line:
                print line
                assert line[0] == ">"
                sequence = input_stream.readline()
                sequence = sequence.rstrip("\n")
                if 'x' in sequence:
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Invalid Characters in Sequence \n" + sequence + "\n")
                    line = input_stream.readline()
                    continue;
                if sequence[0] != 'M' and self.__ms__:
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Sequence Does Not Start With M \n" + sequence + "\n")
                    line = input_stream.readline()
                    continue
                if 'X'*(self.__xs__ + 1) in sequence:
                    # print sequence
                    # print 'X'*(self.__xs__ + 1)
                    # print str(self.__xs__ + 1)
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Sequence Has Too Many Xs \n" + sequence + "\n")
                    line = input_stream.readline()
                    continue
                with open(output_file, "a") as out_stream:
                    out_stream.write(line + sequence + "\n")
                line = input_stream.readline()