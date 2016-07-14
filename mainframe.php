
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
                                <table border=1>
                                    <tr>
                                        <td><b>Sequence Length:</b>
                                    </tr>
                                    <tr>
                                        <td>
                                            Minimum (m):
                                            <input type="text" name="min" value="30"></input>
                                            Maximum (n):
                                            <input type="text" name="max" value="30000"></input>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="descript">Catch sequences that are less <b>m</b> or more than <b>n</b> amino acids long.</td>
                                    </tr>
                                    
                                    <tr>
                                        <td><b>Intra-Sequence Complexity:</b></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            Complexity (c):
                                            <input type="text" name="zj" value="0.9"></input>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="descript">Sequences compressible at least down to <b>c</b> of the original length (repetitive structure)
                                    </tr>

                                    <tr>
                                        <td><b>Inter-Sequence Redundancy:</b></td>
                                    <tr>
                                        <td>
                                            Identity (t):
                                            <input type="text" name="ct" value="0.7"></input>
                                            Fractional Length (f):</td>
                                            <input type="text" name="cl" value="0.8"></input>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="descript">Catch sequences contained with atleast <b>t</b> sequence identity within up to <b>f</b> fractional length of another sequence in this set.
                                    </tr>

                                    <tr>
                                        <td><b>Miscellaneous Settings:</b></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            "X" tolerance (x):
                                            <input type="text" name="xs" value="0"></input>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="descript">Catch sequences with regions containing more than <b>x</b> consecutive "X"s</td>
                                    </tr>
                                    <tr>
                                        <td><input type="checkbox" name="ms"> Check for M at beginning of sequence? </td>
                                    </tr>
                                    <tr>
                                        <td><input type="checkbox" name="dlen"> Bypass Length Filter? </td>
                                    </tr>
                                    <tr>
                                        <td><input type="checkbox" name="dcomp"> Bypass Intra-Sequence Complexity Filter? </td>
                                    </tr>
                                    <tr>
                                        <td><input type="checkbox" name="dred"> Bypass Inter-Sequence Redundancy Filter? </td>
                                    </tr>
                                </table>
                                <div style="height:20px;"></div>
                                
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