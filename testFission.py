from fissionfilter import FissionFilter
f = FissionFilter("test/xenopus_tropicalis.fa")
f.filter_crap("test/sturgeon.fa", "test/sturgeon.clean", "test/sturgeon.messy")