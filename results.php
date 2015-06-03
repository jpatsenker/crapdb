<?php
        $fastaCheck = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl';

        
	if(!$_POST['email']){
            echo '<p style="color:#FF0000">  Please fill in all fields </p>';
    	}else{
            $email = $_POST['email'];
            $target_dir = "uploaded_fasta/";
            $target_file = $target_dir . basename($_FILES['fastaseq']['name']);
            unset($target_dir);

            if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
                    echo '<p style="color:#FF0000"> Bad File </p>';
            }else{

                exec('perl ' . $fastaCheck . ' ' . $target_file . ' 0 > ' . $target_file);
                

                $headers = "From: CRAP DB <noreply@kirschner.med.harvard.edu>" . "\r\n";
                if(mail($email, "CRAP Results", "this is your crap score: 1", $headers)){
                        echo '<p style="color:green"> Sending email with results to ' . $email . ' </p>';
                }
                unlink($target_file);
                unset($target_file);
            }
    	}
    
    
    include "index.html";

?>
