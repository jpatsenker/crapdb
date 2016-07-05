<?php
	$servername = "localhost";
	$username = "jp263";
	$password = "ronda,1n,ropesM";

	// Create connection
	$conn = mysqli_connect($servername, $username, $password);

	// Check connection
	if (!$conn) {
	    die("Connection failed: " . mysqli_connect_error());
	}
	echo "Connected successfully";
?>