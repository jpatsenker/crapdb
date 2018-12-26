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
    echo '<table style="margin:0 auto;"><tr><td>';
    print_r($_POST);
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
    $next_id = rand(1,1000000);
    $fname = $_FILES['fastaseq']['name'];
    $target_fname = substr($fname,0,strpos($fname,'.')) . '_' . $next_id;
    $target_file = $target_dir . $target_fname;


    #move file into uploaded folder
    if(!move_uploaded_file($_FILES['fastaseq']['tmp_name'], $target_file)){
        echo '<div class="notout">';
        echo 'Error Uploading Input File <br>';

    }

?>

    </BODY>
</HTML>