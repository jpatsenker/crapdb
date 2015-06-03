<?php
        $fastaCheck = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl';
        $score = 0;
        
	if(!$_POST['email']){
            echo '<p style="color:#FF0000">  Please fill in all fields </p>';
    	}else{
            $email = $_POST['email'];
            $target_dir = "uploaded_fasta/";
            $target_file = $target_dir . basename($_FILES['fastaseq']['name']);
            $fixed_file = $target_dir . 'fix_' . basename($_FILES['fastaseq']['name']);

            if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
                echo '<p style="color:#FF0000"> Bad File </p>';
            }else{
                echo 'bsub -q short -K -o' . $fixed_file . ' -e tmp/errors.txt perl ' . $fastaCheck . ' ' . $target_file . ' 0';
                exec('bsub -q short -K -o' . $fixed_file . ' -e tmp/errors.txt perl ' . $fastaCheck . ' ' . $target_file . ' 0');
                
                
                
                $fastaFile = fopen($fixed_file, "r");
                $stderr = fopen("tmp/errors.txt", "r");

                if(filesize("tmp/errors.txt") != 0){
                    $score = 1;
                    echo '<p style="color:#FF9933"> Warning: File Was Modified by FASTA Checker</p>';
                }

                $headers = "From: CRAP DB <noreply@kirschner.med.harvard.edu>" . "\r\n";
                if(mail($email, "CRAP Results", "this is your crap score: " . $score, $headers)){
                    echo '<p style="color:green"> Sending email with results to ' . $email . ' </p>';
                }
                //unlink($target_file);
            }
    	}
    
    
    include "index.php";

?>
