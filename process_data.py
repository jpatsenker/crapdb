import sys
import io
import os
import subprocess


#launch from main dir

fastaChecker = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl';

input_file = sys.argv[1]

checked_file = input_file[:input_file.rfind('.')] + '_checked' + input_file[input_file.rfind('.'):]





#PERFORM A FASTA CHECK
process_fastaCheck = subprocess.Popen('bsub -q short -K -W 1 -o ' + fixed_file + ' -e ../tmp/errors.txt perl ' + fastaChecker + ' ' + target_file + ' 0')


process_fastaCheck.wait()

fopen('tmp/errors.txt')



#ADD LENGTHS TO THE FILE

file_with_lengths = checked_file[:input_file.rfind('.')] + '_lengths' + checked_file[input_file.rfind('.'):]


