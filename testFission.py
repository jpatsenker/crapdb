from fission_filter import FissionFilter
f = FissionFilter("test/xenopus_tropicalis.fa")
f.filter_crap("test/sturgeon.fa.fix", "test/sturgeon.clean", "test/sturgeon.messy")