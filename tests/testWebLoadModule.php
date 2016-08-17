<?php
	
	echo "<HTML><HEAD><TITLE>TEST</TITLE><HEAD><BODY>";


	echo "Testing Load Module of seq/hmmer/3.1 <br>";
	exec 'module load seq/hmmer/3.1 > superlog';
	echo "Load Module Complete <p>";

	echo "Testing phmmer (expect usage explanation) <br>";
	#exec 'phmmer > superlog';
	echo "PHMMER Complete <p>";

	echo "</BODY></HTML>";

?>