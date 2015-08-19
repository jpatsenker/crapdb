
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
                                <textarea name="email"></textarea>
                                <p><b>PARAMETERS</b></p>
                                CD-HIT Threshold: 
                                <textarea name="ct">0.7</textarea><br>
                                CD-HIT Fractional Length:
                                <textarea name="cl">0.8</textarea><br>
                                0j Minimum Complexity: 
                                <textarea name="zj"></textarea><br>
                                Minimum Length: 
                                <textarea name="min"></textarea><br>
                                Maximum Length: 
                                <textarea name="max"></textarea><p>
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