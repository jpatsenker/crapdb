<?php

        function get_next_id(){
            $file_handle = fopen("INCREMENTFILE.num", "r+");
            while (!flock($file_handle, LOCK_EX)){}
            $id = fread($file_handle);
            if ($id === NULL){
                $id = 0;
            }
            $next = ($id+1)%1000000;
            ftruncate($file_handle, 0);
            fwrite($file_handle, $next);
            flock($file_handle, LOCK_UN);
            fclose($file_handle);
            return $id;
        }
        
        echo "test";
        
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
                #echo 'python process_crap.py ' . $target_file . ' ' . $target_file . '.clean ' . $target_file . '.messy ' . $email . ' > /dev/null 2>&1 &';
                exec('python process_crap.py ' . $target_file . ' ' . $target_file . '.clean.txt ' . $target_file . '.messy.txt ' . $email . ' > /dev/null 2>&1 &');
                
                echo '<p style="color:green"> You will receive an email when your CRAP is ready. </p>';
                echo '<p><a href="logs/' . $next_id . '"> Log file for job </a></p>';
            }
    	}
    
    
    include "index.php";

?>
