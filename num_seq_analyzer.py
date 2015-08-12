from sewageanalyzer import SewageAnalyzer


class NumSeqAnalyzer(SewageAnalyzer):

    __name__ = "NUMBER_SEQUENCES_ANALYZER"


    def analyze_crap(self, input_file, analysis_file, graphic=False):
        with open(input_file, "r") as input_stream:
            every = input_stream.read()
            stuff = every.split("\n")
            num_seq = int(len(stuff)/2)
        with open(analysis_file, "w") as analysis_stream:
            analysis_stream.write(str(num_seq))