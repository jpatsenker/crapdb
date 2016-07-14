
<div style="width:100%;">
    <table>
        <tr>
            <td>
                <div class="bigblock">
                    <div class="subtitle"> <b>C</b>omprehensive <b>R</b>edundancy <b>A</b>nalysis for Complete Proteomes </div>

                    <div class="general">
                        <form name="download" action="results.php" method="POST" enctype="multipart/form-data">
                            <div id="download_area">
                                <br><b>FASTA: </b> <input type="file" name="fastaseq"><p>
                                <b>EMAIL: </b> <input type="text" name="email"></input>
                                <p><b>PARAMETERS</b></p>
                                <table>
                                    <tr>
                                        <td><b>SEQUENCE LENGTH SETTINGS:</b>
                                    </tr>
                                    <tr>
                                        <td>Minimum (m): </td>
                                        <td><input type="text" name="min" value="30"></input></td>
                                        <td>Maximum (n): </td>
                                        <td><input type="text" name="max" value="30000"></input></td>
                                    </tr>
                                    <tr>
                                        <td>Catch sequences that are less <b>m</b> or more than <b>n</b> amino acids long.</td>
                                    </tr>
                                    
                                    <tr>
                                        <td><b>INTRA-SEQUENCE COMPLEXITY SETTINGS</b></td>
                                    </tr>
                                    <tr>
                                        <td>Complexity (c): </td>
                                        <td><input type="text" name="zj" value="0.9"></input></td>
                                    </tr>
                                    <tr>
                                        <td>Sequences compressible at least down to <b>c</b> of the original length (repetitive structure)
                                    </tr>

                                    <tr>
                                        <td><b>INTER-SEQUENCE REDUNDANCY SETTINGS</b></td>
                                    <tr>
                                        <td>Identity (t):</td>
                                        <td><input type="text" name="ct" value="0.7"></input></td>
                                        <td>Fractional Length (f):</td>
                                        <td><input type="text" name="cl" value="0.8"></input></td>
                                    </tr>
                                    <tr>
                                        <td>Catch sequences contained with atleast <b>t</b> sequence identity within up to <b>f</b> fractional length of another sequence in this set.
                                    </tr>

                                    <tr>
                                        <td><b>MISC. SETTINGS</b></td>
                                    </tr>
                                    <tr>
                                        <td>"X" tolerance (x):</td>
                                        <td><input type="text" name="xs" value="0"></input></td>
                                    </tr>
                                    <tr>
                                        <td>Catch sequences with regions containing more than <b>x</b> consecutive "X"s</td>
                                    </tr>
                                </table>
                                <div style="height:20px;"></div>
                                <input type="checkbox" name="ms"> Check for M at beginning of sequence? <br>
                                <input type="checkbox" name="dlen"> Bypass Length Filter? <br>
                                <input type="checkbox" name="dcomp"> Bypass Intra-Sequence Complexity Filter? <br>
                                <input type="checkbox" name="dred"> Bypass Inter-Sequence Redundancy Filter? <br>
                                <p></p>
                                <input type="submit"/>
                            </div>
<p>
                        </form>
                    </div>
                </div>
            </td>
    </table>
</div>