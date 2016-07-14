import logtools

def fix_file(input_file, output_file, lfil = None):
    if lfil is not None:
        logtools.add_to_log("INTERNAL REFORMATTING", lfil, description="Running Reformat, file transition: " + input_file + " -> " + output_file)
        logtools.add_big_description("*Removing newline characters from sequences in file\n*Creating new file " + output_file + " to store formatted file", lfil)
        logtools.add_start(lfil)
    with open(input_file, "r") as ifile:
        ifile.read(1)
        with open(output_file, "w") as ofile:
            while True:
                datum = ""
                final = ifile.read(1)
                nl = False
                while (final != ">" or not nl) and final != "":
                    datum += final
                    if final == "\n":
                        nl = True
                    final = ifile.read(1)
                if datum == "":
                    break;

                if datum.isspace() or len(datum) == 0:
                    continue
                ofile.write(">")
                desc_end = datum.find("\n")
                seq_start = desc_end
                while seq_start<len(datum) and datum[seq_start].isspace():
                    seq_start+=1
                seqTmp = datum[seq_start:]
                seq = "".join(seqTmp.split())
                ofile.write(datum[:desc_end] + "\n" + seq + "\n")
    if lfil is not None:
        logtools.add_end(lfil)