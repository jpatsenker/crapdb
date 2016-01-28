# crapdb
Website for calculating CRAP of given proteome

Parameters:

"-0j #" - Set minimum complexity (default .9)
"-ct #" - Set threshold for running CD-HIT (default .7)
"-cl #" - Set fractional length for redundancy filtering (default .8)
"-min #" - Set minimum length (default 30)
"-max #" - Set maximum length (default 30000)
"-fft #" - Set threshold for running CD-HIT in Fusion/Fission filter (default .7)
"-ffl #" - Set fractional length (bottom) for fusion/fission filtering (default .8)
"-xs #" - Maximum number of consecutive Xs in sequence to ignore (default 0)
"-ms" - Check for M as first amino acid (default does not check)
"-nolen" - Destage length filter (default completes stage)
"-nocomp" - Destage complexity (0j) filter (default completes stage)
"-nored" - Destage redundancy (CD-HIT) filter (default completes stage)
"-noff" - Destage fusion/fission (Ff) filter (default completes stage)