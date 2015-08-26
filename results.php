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
            if (!flock($file_handle, LOCK_EX)){
                print "Please reset INCREMENTFILE.num, php flock() error";
                exit(1);
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
        #echo '<div>';
	if(!$_POST['email']){
            echo '<div class="notout">';

            echo '<p>  Please fill in all fields </p>';
    	}else{
            #get information
            $email = $_POST['email'];
            $ct = $_POST['ct'];
            $cl = $_POST['cl'];
            $min = $_POST['min'];
            $max = $_POST['max'];
            #$compl = $_POST['compl'];
            $zj = $_POST['zj'];
            $xs = $_POST['xs'];
            $ms = $_POST['ms'];
            $fft = $_POST['fft'];
            $ffl = $_POST['ffl'];
            
//            if ($compl != "on"){
//                $compl = " -nocomp ";
//            }else{
//                $compl = "";
//            }
            if ($ms != "on"){
                $ms = " -ms ";
            }else{
                $ms = "";
            }
            
            
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

                $fullpath = substr(getcwd(),strpos(getcwd(), "/www/") + 5) . "/logs/" . $next_id . ".log";
                $fullpath = str_replace("/docroot/", "/", $fullpath);
                mail($email, "CRAP REQUEST SENT", "We are processing your file as: " . $target_file . " size: " . filesize($target_file) . ' bytes.<br> ' . $fullpath . '<br>', $headers);
                
                echo "<p> We are processing your file as: " . $target_file . " size: " . filesize($target_file) . " bytes </p>";
                echo 'python process_crap_interface.py ' . $target_file . ' ' . $target_file . '.clean.txt ' . $target_file . '.messy.txt ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . ' -fft ' . $fft . ' -ffl ' . $ffl . $ms . '-xs ' . $xs . ' > superlog 2>&1 &';
                exec('python process_crap_interface.py ' . $target_file . ' ' . $target_file . '.clean.txt ' . $target_file . '.messy.txt ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . ' -fft ' . $fft . ' -ffl ' . $ffl . $ms . '-xs ' . $xs . ' > superlog 2>&1 &');
                
                echo '<p> You will receive an email when your CRAP is ready. </p>';
                echo '<p><a href="logs/' . $next_id . '.log"> Log file for job </a></p>';
            }
            
    	}
    
    echo "</div></td></tr></table>";

    include "mainframe.php";

?>

    </BODY>
</HTML>