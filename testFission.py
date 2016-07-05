from fission_filter import FissionFilter
f = FissionFilter("test/xenopus_tropicalis.fa")
f.filter_crap("test/sturgeon.fa.fix", "test/sturgeon2.clean", "test/sturgeon2.messy")


#bsub -q parallel -K -W 4:00 -o test/testParallel.stdout -e test/testParallel.stderr -n 50 -R "rusage[mem=2000]span[ptile=8]" -o test/test.stdout -e test/test.stderr phmmer --domtblout test/sturgeon_frog.hmmerOut test/sturgeon.fa test/xenopus_tropicalis.fa