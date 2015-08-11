<?php

        function get_next_id(){
            return 0;
        }
        

        $fastaCheck = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl';
        $score = 0;
        
        parse_ini_file("php.ini");
        
	if(!$_POST['email']){
            echo '<p style="color:#FF0000">  Please fill in all fields </p>';
    	}else{
            #get information
            $email = $_POST['email'];
            $target_dir = "uploaded_fasta/";
            $next_id = get_next_id();
            $target_file = $target_dir . $next_id;
            
            #move file into uploaded folder
            if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
                echo '<p style="color:#FF0000"> Error Moving File </p>';
            }else{
                mail($email, "CRAP REQUEST SENT", "We are processing your file as: " . $target_file . " size: " . filesize($target_file) . " bytes", 'From: "CRAP DB" <noreply@kirschner.med.harvard.edu>');
                echo "We are processing your file as: " . $target_file . " size: " . filesize($target_file) . " bytes";
                exec('python process_data.py ' . $target_file . ' ' . $email . ' > /dev/null 2>&1 &');
                
                echo '<p style="color:green"> You will receive an email when your CRAP is ready. </p>';
            }
    	}
    
    
    include "index.php";

?>
