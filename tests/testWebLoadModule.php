<?php
	
	echo "<HTML><HEAD><TITLE>TEST</TITLE><HEAD><BODY>";

	echo "Initial test phmmer (expect error) <br>";
	#exec 'phmmer > superlog 2>&1 &';
	echo "PHMMER Complete <p>";

	echo "Testing Load Module of seq/hmmer/3.1 <br>";
	#exec 'module load seq/hmmer/3.1 > superlog 2>&1 &';
	echo "Load Module Complete <p>";

	echo "Testing phmmer (expect usage explanation) <br>";
	#exec 'phmmer > superlog 2>&1 &';
	echo "PHMMER Complete <p>";

	echo "</BODY></HTML>";

?>