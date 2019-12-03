import os

#INTERPRETERS/COMPILERS
PYTHON_PATH = 'python' #'/usr/bin/python'
PERL_PATH = 'perl' #'/usr/bin/perl'

SITENAME = os.getenv('SITENAME', default='corecop.hms.harvard.edu')
SITE_DOCROOT = os.getenv('SITE_DOCROOT', default=os.path.join('/www', SITENAME, 'docroot'))
CORECOP = os.getenv('CORECOP', default='corecop')
CORECOP_DIR = os.path.join(SITE_DOCROOT, CORECOP)

#RELEVANT SCRIPTS
#FASTACHECKER_PATH = os.path.join(SITE_DOCROOT, 'genomes/code/fasta_checker_for_crap.pl')
FASTACHECKER_PATH = os.path.join(CORECOP_DIR, 'analyzers/fasta_checker_for_crap.pl')
CDHIT_PATH = os.path.join(CORECOP_DIR, 'aux/run_cd-hit.sh')
ZEROJ_PATH = os.path.join(CORECOP_DIR, '0j/0j.py')
