<script type="text/javascript">
    function toggle(input){
        var x = document.getElementById(input);
        if (x.style.display == "none"){
            x.style.display = "block";
            } else {
            x.style.display = "none";
        }
    }
</script>

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
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title">
                                                        <b>Sequence Length: </b>
                                                        <a href="javascript:toggle('Length_Description')">(?)</a>
                                                    </td>
                                                    <td>
                                                        <input type="checkbox" name="dlen"> Bypass?
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = "Length_Description" style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences that are less that <b>m</b> or more than <b>n</b> amino acids long.</td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        Minimum (m):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="min" value="30" class="param"></input>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        Maximum (n):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="max" value="30000" class="param"></input>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title"><b>Intra-Sequence Complexity: </b><a href="javascript:toggle('ISC_Description')">(?)</a></td><td><input type="checkbox" name="dcomp"> Bypass? </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = "ISC_Description" style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences compressible at least down to <b>c</b> of the original length (repetitive structure)
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        Complexity (c):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="zj" value="0.9" class="param"></input>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title"><b>Inter-Sequence Redundancy: </b><a href="javascript:toggle('ISR_Description')">(?)</a></td><td> <input type="checkbox" name="dred"> Bypass? </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = 'ISR_Description' style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences contained with atleast <b>t</b> sequence identity within up to <b>f</b> fractional length of another sequence in this set.
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        Identity (t):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="ct" value="0.7" class="param"></input>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        Fractional Length (f):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="cl" value="0.8" class="param"></input>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting_title"><b>Fission: </b><a href="javascript:toggle('FIS_Description')">(?)</a></td><td> <input type="checkbox" name="dfis"> Bypass? </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = 'FIS_Description' style="display: none;width: 20em;">
                                        <td class="descript setting">Flag sequences that are potentially joinable fragments of <b>Reference Genome</b>.
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    Reference Genome:
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        <input type="checkbox" name="human"> Homo Sapiens
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td>
                                                        <input type="checkbox" name="xtrop"> Xenopus Tropicalis
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="setting">
                                                        ADD FILE HERE
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>Miscellaneous Settings:</b></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td class="setting">
                                                        "X" tolerance (x):
                                                    </td>
                                                    <td>
                                                        <input type="text" name="xs" value="0" class="param"></input>
                                                        <a href="javascript:toggle('XS_Description')">(?)</a>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr id = 'XS_Description' style="display: none;width: 20em">
                                        <td class="descript setting">Flag sequences with regions containing more than <b>x</b> consecutive "X"s</td>
                                    </tr>
                                    <tr>
                                        <td><input type="checkbox" name="ms"> Check for M at beginning of sequence? </td>
                                    </tr>                       
                                </table>
                                <div style="height:20px;"></div>
                                
                                <p></p>
                                <input type="submit"/>
                            </div>
                            <p>
                            <div style="font-size:50%;">
                                <b>Contact:</b><i><br>moc.liamg@nikhsep backwards<br>moc.reknestap@nahtanoj backwards</i>
                            </div>
                        </form>
                    </div>
                </div>
            </td>
    </table>
</div>