from sewageanalyzer import SewageAnalyzer


class SeqLengthAnalyzer(SewageAnalyzer):

    __name__ = "LENGTH_DISTRIBUTION_ANALYZER"

    def analyze_crap(self, input_file, analysis_file, graphic=True):
        lengths = {}
        with open(input_file, "r") as input_stream:
            line = input_stream.readline()
            while line:
                assert line[0] == ">"
                sequence = input_stream.readline()
                sequence = sequence.rstrip("\n")
                try:
                    lengths[len(sequence)] += 1
                except KeyError:
                    lengths[len(sequence)] = 1
                line = input_stream.readline()
        with open(analysis_file, "w") as analysis_stream:
            for l in lengths:
                analysis_stream.write(str(l) + "," + str(lengths[l]) + "\n")
