<!DOCTYPE html>
<?php parse_ini_file("php.ini"); //phpinfo();?>

<html>

    <head>
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <title>
            CRAP
        </title>
    </head>

    <body>
        <div class="bigblock">
            <div class="headline"> crap web server</div>

            <form name="download" action="results.php" method="POST" enctype="multipart/form-data">

                <div id="download_area">
                    <p><b>FASTA</b></p>
                    <input type="file" name="fastaseq">
                    <p><b>EMAIL</b></p>
                    <textarea name="email"></textarea>
                    <p></p>
                    <input type="submit"/>
                </div>
            </form>
        </div>
    </body>





</html>
