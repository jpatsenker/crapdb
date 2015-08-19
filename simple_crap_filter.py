from sewagefilter import SewageFilter


class SimpleFilter(SewageFilter):

    __name__ = "SIMPLE_CRAP_FILTER"


    def filter_crap(self, input_file, output_file, diagnostics_file):
        open(output_file, "w").close()
        with open(input_file, "r") as input_stream:
            line = input_stream.readline()
            while line:
                assert line[0] == ">"
                sequence = input_stream.readline()
                sequence = sequence.rstrip("\n")
                if 'X' in sequence:
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Invalid Characters in Sequence " + sequence + "\n")
                    continue
                if sequence[0] != 'M':
                    with open(diagnostics_file, "a") as diag_stream:
                        diag_stream.write(line.rstrip("\n") + " Sequence Does Not Start With M " + sequence + "\n")
                    continue
                with open(output_file, "a") as out_stream:
                    out_stream.write(line + sequence + "\n")
                line = input_stream.readline()