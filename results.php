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
    error_reporting(E_ALL); // Error engine - always ON!
    ini_set('display_errors', TRUE); // Error display - OFF in production env or real server
    ini_set('log_errors', TRUE); // Error logging
    ini_set('error_log', '/www/kirschner.med.harvard.edu/docroot/corecop/log/webserver_php_errors.log'); // Logging file
    ini_set('log_errors_max_len', 1024); // Logging file size

    error_log('hello world');
    $headers = 'From: "CoreCop Pipeline" <noreply@kirschner.med.harvard.edu>\r\n';
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";

    $sent = mail($email, "CoreCop REQUEST SENT", "hello world", $headers);

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
    
    $target_dir = "uploaded_fasta/";
    $next_id = rand(1,PHP_INT_MAX);
    $fname = $_FILES['fastaseq']['name'];
    $target_fname = substr($fname,0,strpos($fname,'.')) . '_' . $next_id;
    $target_file = $target_dir . $target_fname;


    #move file into uploaded folder
    if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
        echo '<div class="notout">';
        echo 'Error Uploading Input File <br>';

    }else{
        echo '<div class="outputs">';
        echo '<p>Sending Mail...</p>';
        if($_POST['email']){
            $headers = 'From: "CoreCop Pipeline" <noreply@kirschner.med.harvard.edu>\r\n';
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";

            $fullpath = substr(getcwd(),strpos(getcwd(), "/www/") + 5) . "/logs/" . $target_fname . ".log";
            $fullpath = str_replace("/docroot/", "/", $fullpath);
            $sent = @mail($email, "CoreCop REQUEST SENT", "We are processing your file as: " . $target_file . " size: " . filesize($target_file) . ' bytes.<br> ' . $fullpath . '<br>', $headers);
            if($sent){
                echo "<p> Email Validated... </p>";
            }else{
                echo "<p> INVALID EMAIL! SEE LINK BELOW</p>";
                #echo '<form action="index.php"><input type="button" value="Back" onClick="history.go(-1);return true;"></form>';
                #echo "</div></td></tr></table>";
                #die();
            }
        }

        echo "<p> Your file in our system: " . $target_file . " size: " . filesize($target_file) . " bytes </p>";
        echo 'python run_cra_interface.py ' . $target_file . ' ' . $target_file . '.clean.fa ' . $target_file . '.messy.fa ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . $ms . ' -xs ' . $xs . $dComp . $dLen . $dRed .' > superlog 2>&1 &';
        exec('python run_cra_interface.py ' . $target_file . ' ' . $target_file . '.clean.fa ' . $target_file . '.messy.fa ' . $email . ' -ct ' . $ct . ' -cl ' . $cl . ' -0j ' . $zj . ' -min ' . $min . ' -max ' . $max . $ms . ' -xs ' . $xs . $dComp . $dLen . $dRed .' > superlog 2>&1 &');

        if($_POST['email']){
            echo '<p> You will receive an email when the results are ready. </p>';
        }
        echo '<p><a href="logs/' . $target_fname . '.log"> Log file for job </a></p>';

    }

    echo '<form action="index.php"><input type="button" value="Back" onClick="history.go(-1);return true;"></form>';

    echo "</div></td></tr></table>";

?>

    </BODY>
</HTML>