
<div style="width:100%;">
    <table>
        <tr>
            <td>
                <div class="bigblock">
                    <a href="index.php">
                        <div class="headline">C.R.A.P. web server</div> <p>
                    </a>
                    <div class="subtitle"> <b>C</b>omprehensive <b>R</b>edundancy <b>A</b>nalysis for Complete <b>P</b>roteomes </div>

                    <div class="general">
                        <form name="download" action="results.php" method="POST" enctype="multipart/form-data">

                            <div id="download_area">
                                <p><b>FASTA</b></p>
                                <input type="file" name="fastaseq">
                                <p><b>EMAIL</b></p>
                                <input type="text" name="email"></input>
                                <p><b>PARAMETERS</b></p>
                                CD-HIT Threshold: 
                                <input type="text" name="ct" value="0.7"></input><br>
                                CD-HIT Fractional Length:
                                <input type="text" name="cl" value="0.8"></input><br>
                                0j Minimum Complexity: 
                                <input type="text" name="zj" value="0.9"></input><br>
                                Minimum Length: 
                                <input type="text" name="min" value="30"></input><br>
                                Maximum Length: 
                                <input type="text" name="max" value="30000"></input><p>
                                <input type="checkbox" name="compl" checked> Completeness? <br>
                                <p></p>
                                <input type="submit"/>
                            </div>
                        </form>
                    </div>
                </div>
            </td>
    </table>
</div>