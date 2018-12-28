<?php 
    $ini_array=parse_ini_file('php.ini');
    if($ini_array){
        echo "Success";
        print_r($ini_array);
    }else{
        echo "Failure";
    }
    
    print_r(ini_get_all());
    
    phpinfo();

?>