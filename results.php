<HTML>
    <HEAD>
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <title>
            CRAP
        </title>
        
    </HEAD>
    <BODY>


<?php

        function get_next_id(){
            $file_handle = fopen("INCREMENTFILE.num", "r+");
            while (!flock($file_handle, LOCK_EX)){
                sleep(1);
            }
            $id = stream_get_contents($file_handle);
            $next = ($id+1)%10000;
            fseek($file_handle,0);
            ftruncate($file_handle,0);
            fwrite($file_handle, $next);
            flock($file_handle, LOCK_UN);
            fclose($file_handle);
            return $id;
        }
        
        
        parse_ini_file("php.ini");
        
        echo '<table><tr><td>';
        
	if(!$_POST['email']){
            echo '<div class="notout">';

            echo '<p>  Please fill in all fields </p>';
    	}else{
            #get information
            $email = $_POST['email'];
            $target_dir = "uploaded_fasta/";
            $next_id = get_next_id();
            $target_file = $target_dir . $next_id;
                     
            
            
            #move file into uploaded folder
            if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
                echo '<div class="notout">';
                echo 'Error Moving File <br>';
            }else{
                echo '<div class="outputs">';

                $headers = 'From: "CRAP Pipeline" <noreply@kirschner.med.harvard.edu>\r\n';
                $headers .= "MIME-Version: 1.0\r\n";
                $headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";

                
                mail($email, "CRAP REQUEST SENT", "We are processing your file as: " . $target_file . " size: " . filesize($target_file) . ' bytes.<br> <a href="' . "logs/" . $next_id . ".log" . '.log"> Log file for job </a>', $headers);
                
                echo "<p> We are processing your file as: " . $target_file . " size: " . filesize($target_file) . " bytes </p>";
                #echo 'python process_crap.py ' . $target_file . ' ' . $target_file . '.clean ' . $target_file . '.messy ' . $email . ' > /dev/null 2>&1 &';
                exec('python process_crap.py ' . $target_file . ' ' . $target_file . '.clean.txt ' . $target_file . '.messy.txt ' . $email . ' > /dev/null 2>&1 &');
                
                echo '<p> You will receive an email when your CRAP is ready. </p>';
                echo '<p><a href="logs/' . $next_id . '.log"> Log file for job </a></p>';
            }
            
    	}
    
    echo "</div></td></tr></table>";

    include "mainframe.php";

?>

    </BODY>
</HTML>