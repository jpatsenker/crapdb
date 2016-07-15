<HTML>
    <HEAD>
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <title>
            CRA
        </title>
        
    </HEAD>
    <BODY>


<?php

        function get_next_id(){
            $file_handle = fopen("INCREMENTFILE.num", "r+");
            while (!flock($file_handle, LOCK_EX)){
                //print "Please reset INCREMENTFILE.num, php flock() error";
                //exit(1);
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
            $dComp = $_POST['dcomp'];
            $dRed = $_POST['dred'];
            $dLen = $_POST['dlen'];
            $dFf = $_POST['dff'];
            $zj = $_POST['zj'];
            $xs = $_POST['xs'];
            $ms = $_POST['ms'];
            $fft = $_POST['fft'];
            $ffl = $_POST['ffl'];
            
            if ($dLen == "on"){
                $dLen = " -nolen ";
            }else{
                $dLen = "";
            }
            if ($dRed == "on"){
                $dRed = " -nored ";
            }else{
                $dRed = "";
            }
            if ($dComp -= "on"){
                $dComp = " -nocomp ";
            }else{
                $dComp = "";
            }
            if ($dFf == "on"){
                $dFf = " -noff ";
            }else{
                $dFf = "";
            }
            if ($ms == "on"){
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
                echo '<form action="index.php"><input type="submit" value="Back"></form>';

            }else{
                echo '<div class="outputs">';

                $headers = 'From: "CRAP Pipeline" <noreply@kirschner.med.harvard.edu>\r\n';
                $headers .= "MIME-Version: 1.0\r\n";
                $headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";

                $fullpath = substr(getcwd(),strpos(getcwd(), "/www/") + 5) . "/logs/" . $next_id . ".log";
                $fullpath = str_replace("/docroot/", "/", $fullpath);
                mail($email, "CRAP REQUEST SENT", "We are processing your file as: " . $target_file . " size: " . filesize($target_file) . ' bytes.<br> ' . $fullpath . '<br>', $headers);
                
                echo "<p> We are processing your file as: " . $target_file . " size: " . filesize($target_file) . " bytes </p>";
                echo 'python process_crap_interface.py ' . $target_file . ' ' . $target_file . '.clean.txt ' . $target_file . '.messy.txt ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . $ms . ' -xs ' . $xs . $dComp . $dLen . $dRed . $dFf .' > superlog 2>&1 &';
                exec('python process_crap_interface.py ' . $target_file . ' ' . $target_file . '.clean.txt ' . $target_file . '.messy.txt ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . $ms . ' -xs ' . $xs . $dComp . $dLen . $dRed . $dFf .' > superlog 2>&1 &');
                
                echo '<p> You will receive an email when the results are ready. </p>';
                echo '<p><a href="logs/' . $next_id . '.log"> Log file for job </a></p>';
                echo '<form action="index.php"><input type="submit" value="Back"></form>';

            }
            
    	}
    
    echo "</div></td></tr></table>";

?>

    </BODY>
</HTML>