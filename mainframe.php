
<div style="width:100%;">
    <table>
        <tr>
            <td>
                <div class="bigblock">
                    <div class="subtitle"> <b>C</b>omprehensive <b>R</b>edundancy <b>A</b>nalysis for Complete <b>P</b>roteomes </div>

                    <div class="general">
                        <form name="download" action="results.php" method="POST" enctype="multipart/form-data">
                            <div id="download_area">
                                <br><b>FASTA: </b> <input type="file" name="fastaseq"><p>
                                <b>EMAIL: </b> <input type="text" name="email"></input>
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
                                <input type="text" name="max" value="30000"></input><br>
                                Maximum Number of "X"s to be ignored:
                                <input type="text" name="xs" value="0"></input><br>
                                Fusion/Fission Threshold:
                                <input type="text" name="fft" value="0.7"></input><br>
                                Fusion/Fission Fractional Length:
                                <input type="text" name="ffl" value="0.8"></input><p>
                                <input type="checkbox" name="ms"> Check for M at beginning of sequence? <br>
                                <p></p>
                                <input type="submit"/>
                            </div>
<p>
                    <a href="index.php"><div class="headline">C.R.A. web server</div> <p> </a>
                        </form>
                    </div>
                </div>
            </td>
    </table>
</div>