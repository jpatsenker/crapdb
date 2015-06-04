<?php
        $fastaCheck = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl';
        $score = 0;
        
        parse_ini_file("php.ini");
        
	if(!$_POST['email']){
            echo '<p style="color:#FF0000">  Please fill in all fields </p>';
    	}else{
            #get information
            $email = $_POST['email'];
            $target_dir = "uploaded_fasta/";
            $target_file = $target_dir . basename($_FILES['fastaseq']['name']);
            $fixed_file = $target_dir . 'fix_' . basename($_FILES['fastaseq']['name']);
            
            #move file into uploaded folder
            if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
                echo '<p style="color:#FF0000"> Error Moving File </p>';
            }else{
                echo 'bsub -q short -K -W 1 -o ' . $fixed_file . ' -e tmp/errors.txt perl ' . $fastaCheck . ' ' . $target_file . ' 0';
                #set up orchestra profile
                exec('./opt/lsf/conf/profile.lsf');
                
                #do a fasta check - submitting job to short queue, waiting for it to end, setting 1 hour of wait time, outputing to file, and sending error to another file
                exec('bsub -q short -K -W 1 -o ' . $fixed_file . ' -e tmp/errors.txt perl ' . $fastaCheck . ' ' . $target_file . ' 0');
                
                
                
                $fastaFile = fopen($fixed_file, "r");
                $stderr = fopen("tmp/errors.txt", "r");

                if(filesize("tmp/errors.txt") != 0){
                    $score = 1;
                    echo '<p style="color:red">Error Processing File</p>';
                }
                
                
                

                $headers = "From: CRAP DB <noreply@kirschner.med.harvard.edu>" . "\r\n";
                if(mail($email, "CRAP Results", "this is your crap score: " . $score, $headers)){
                    echo '<p style="color:green"> Sending email with results to ' . $email . ' </p>';
                }
                unlink($target_file);
            }
    	}
    
    
    include "index.php";

?>
