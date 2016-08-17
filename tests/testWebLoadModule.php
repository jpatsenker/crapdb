<?php
	
	echo "Testing Load Module of seq/hmmer/3.1";
	exec 'module load seq/hmmer/3.1 > superlog';
	echo "Load Module Complete";

	echo "Testing phmmer (expect usage explanation)";
	exec 'phmmer > superlog';
	echo "PHMMER Complete";

?>