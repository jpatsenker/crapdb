<HTML>
    <HEAD>
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <title>
            CoreCop
        </title>
        
    </HEAD>
    <BODY>

<?php

    parse_ini_file("php.ini");
    date_default_timezone_set("America/New_York");
    error_reporting(-1);
    #error_reporting(E_ALL); // Error engine - always ON!
    ini_set('display_errors', FALSE); // Error display - OFF in production env or real server
    ini_set('log_errors', TRUE); // Error logging

    function endsWith($haystack, $needle){
        $length = strlen($needle);
        if ($length == 0) {
            return true;
        }
        return (substr($haystack, -$length) === $needle);
    }

    echo '<table style="margin:0 auto;"><tr><td>';
    #get information
    $email = $_POST['email'];    
    $ct = $_POST['ct'];
    $cl = $_POST['cl'];
    $min = $_POST['min'];
    $max = $_POST['max'];
    $dComp = $_POST['dcomp'];
    $dRed = $_POST['dred'];
    $dLen = $_POST['dlen'];
    #$dFis = $_POST['dfis'];
    $zj = $_POST['zj'];
    $xs = $_POST['xs'];
    $ms = $_POST['ms'];
    $ef = $_POST['exfile'];
    #$fft = $_POST['fft'];
    #$ffl = $_POST['ffl'];
    #$rg = $_POST['refgm'];
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
    if ($dComp == "on"){
        $dComp = " -nocomp ";
    }else{
        $dComp = "";
    }
    #if ($dFis == "on"){
    #    $dFis = " -nofis ";
    #}else{
    #    $dFis = "";
    #}
    if ($ms == "on"){
        $ms = " -ms ";
    }else{
        $ms = "";
    }

    if (isset($_SERVER['CORECOP'])){
      $corecop_base = $_SERVER['CORECOP'];
    }else{
      $corecop_base = 'corecop';
    }
    $target_dir = "uploaded_fasta/";
    $next_id = rand(1,PHP_INT_MAX);
    $fname = $_FILES['fastaseq']['name'];
    $target_fname = substr($fname,0,strpos($fname,'.'));
    if($target_fname==""){
        $target_fname = $fname;
    }
    #limit size of file name
    $target_fname = substr($target_fname,0,10);
    #add random num to end of file name
    $target_fname .= '_' . $next_id;
    $target_file = $target_dir . $target_fname;
    
    
    #move file into uploaded folder
    if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
        if($ef){
            $target_fname="test_combined.fa";
            $fname = "test_combined.fa";
            $target_file=$target_dir . $target_fname;
            copy("test_combined.fa",$target_file);
        }else{
            echo '<div class="notout">';
            echo 'Error Uploading Input File <br>';
            die();
        }

    }
    
    echo '<div class="outputs">';
    echo '<p>Sending Mail...</p>';
    if($_POST['email']){
        $headers = 'From: "CoreCop Pipeline" <noreply@kirschner.med.harvard.edu>';
        #$headers .= 'MIME-Version: 1.0\r\n';
        #$headers .= 'Content-Type: text/html; charset=ISO-8859-1\r\n';
	# Prefer https, unless the request has a non-standard port in which case it won't be.
	if (endsWith($_SERVER['HTTP_HOST'], ':80')) {
	    $urlbegin = "https://" . substr($_SERVER['HTTP_HOST'], 0, -3);
	} elseif (endsWith($_SERVER['HTTP_HOST'], ':443')) {
	    $urlbegin = "https://" . substr($_SERVER['HTTP_HOST'], 0, -4);
	}else{
	    $urlbegin = "http://" . $_SERVER['HTTP_HOST'];
	}
        $url = $urlbegin . '/' . $corecop_base . '/logs/' . $target_fname . '.log';
        #$fullpath = substr(getcwd(),strpos(getcwd(), '/www/') + 5) . '/logs/' . $target_fname . '.log';
        #$fullpath = str_replace('/docroot/', '/', $fullpath);
        $sent = mail($email, 'CoreCop REQUEST SENT', 'We are processing your file as: ' . $target_file . ' size: ' . filesize($target_file) . " bytes.\n" . $url . "\n", $headers);
        if($sent){
            echo '<p> Email Sent... </p>';
        }else{
            echo '<p> Couldn\'t send email! See link below... </p>';
            #echo '<form action="index.php"><input type="button" value="Back" onClick="history.go(-1);return true;"></form>';
            #echo "</div></td></tr></table>";
            #die();
        }
    }

    echo '<p> File: ' . $fname . '<br>';
    echo 'Size: ' . filesize($target_file) . ' bytes <br>';
    echo 'ID: ' . $target_fname . '</p>';

    echo gethostname() . '</p>';

    $cmd_str = 'python -v run_cra_interface.py ' . $target_file . ' ' . $target_file . '.clean.fa ' . $target_file . '.messy.fa ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . $ms . ' -xs ' . $xs . $dComp . $dLen . $dRed .' >  log/php_to_python.log 2>&1';
    #exec('python run_cra_interface.py ' . $target_file . ' ' . $target_file . '.clean.fa ' . $target_file . '.messy.fa ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . $ms . ' -xs ' . $xs . $dComp . $dLen . $dRed .' > log/php_to_python.log 2>&1 &');
    echo $cmd_str;        
    exec($cmd_str);
    #exec('python test_python.py > log/php_to_python.log 2>&1 &');
    #exec('whoami > log/php_to_python.log 2>&1');

    if($_POST['email']){
        echo '<p> You will receive an email when the results are ready. <br>';
        echo 'Email ' . $email . '</p>';
    }

    echo '<p> <a href="' . $target_file . '.clean.fa ' . '">Clean Result File</a> Contains remaining sequences (will be available when results are done) <br>';
    echo '<a href="' . $target_file . '.messy.fa ' . '">Annotated Result File</a> Contains filtered and annotated sequences (will be available when results are done) </p>';

    echo '<p><a href="logs/' . $target_fname . '.log"> Log File</a></p>';


?>
    <form action="index.php"><input type="button" value="Back" onClick="history.go(-1);return true;"></form></div></td></tr></table>
    </BODY>
</HTML>
