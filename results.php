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
            
            #move file into uploaded folder
            if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){          
                echo '<p style="color:#FF0000"> Error Moving File </p>';
            }else{
                #echo 'python process_data.py ' . $target_file . ' ' . $email;
                exec('python process_data.py ' . $target_file . ' ' . $email);
                
                echo '<p style="color:green"> Your request is being processed. You will receive an email when your CRAP is ready. </p>';
            }
    	}
    
    
    include "index.php";

?>
