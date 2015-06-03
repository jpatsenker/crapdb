<?php
        $fastaCheck = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl';

        
	if(!$_POST['email']){
            echo '<p style="color:#FF0000">  Please fill in all fields </p>';
    	}else{
            $email = $_POST['email'];
            $target_dir = "uploaded_fasta/";
            $target_file = $target_dir . basename($_FILES['fastaseq']['name']);

            if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
                echo '<p style="color:#FF0000"> Bad File </p>';
            }else{

                $stderr = fopen("errors.txt", "r");
                exec('perl ' . $fastaCheck . ' ' . $target_file . ' 0 > ' . $target_file . ' 2> tmp/errors.txt');
                fopen($target_file, "r");
                if(filesize("tmp/errors.txt") != 0){
                    echo '<p style="color:#FF9933"> Warning: File Was Modified by FASTA Checker</p>';
                }

                $headers = "From: CRAP DB <noreply@kirschner.med.harvard.edu>" . "\r\n";
                if(mail($email, "CRAP Results", "this is your crap score: 1", $headers)){
                    echo '<p style="color:green"> Sending email with results to ' . $email . ' </p>';
                }
                unlink($target_file);
            }
    	}
    
    
    include "index.php";

?>
