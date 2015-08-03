from sewagefilter import SewageFilter
import subprocess


class FastaCheckFilter(SewageFilter):

    __name__ = "FASTA_CHECK_FILTER"

    __fasta_checker__ = "/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl"


    #TODO!!!! Figure out what happens with fasta checker

    def filter_crap(self, input_file, output_file):
        process_fastaCheck = subprocess.Popen(['/bin/bash', '-c',
                                       './run_with_profile.sh -q short -K -W 1 -o ' + output_file + ' -e tmp/fasta_errors.txt perl ' + self.__fasta_checker__ + ' ' + input_file + ' 0 2>tmp/errors.txt'])
        process_fastaCheck.wait()  # wait for fasta to finish before continuing
