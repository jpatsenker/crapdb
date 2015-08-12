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
        <div style="width:100%;">
            <table>
                <tr>
                    <td><div style="width:30%;"></div></td>
                    <td>
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
                    </td>
                    <td><div style="width:30%;"></div></td>
            </table>
        </div>
    </body>





</html>
