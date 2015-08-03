from os.path import basename
from sewagefilter import SewageFilter
import lsftools as lsf


class ComplexityFilter(SewageFilter):

    __name__ = "0J_CHECK_FILTER"

    __zero_j__ = "/www/kirschner.med.harvard.edu/docroot/genomes/code/0j/0j.py"

    def filter_crap(self, input_file, output_file):
        temporary = "tmp/" + basename(input_file)
        lsf.run_job("python " + self.__zero_j__ + " -scores_only " + input_file, output=temporary)
