<HTML>
    <HEAD>
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <title>
            CoreCop
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
    $next_id = get_next_id();

?>

    </BODY>
</HTML>