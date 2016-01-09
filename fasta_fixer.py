def fix_file(input_file, output_file):
    with open(input_file, "r") as ifile:
        everything = ifile.read()
    with open(output_file, "w") as ofile:
        for datum in everything.split(">"):
            print datum
            if datum.isspace() or len(datum) == 0:
                continue
            ofile.write(">")
            desc_end = datum.find("\n")
            seq_start = desc_end
            while seq_start<len(datum) and datum[seq_start].isspace():
                seq_start+=1
            seqTmp = datum[seq_start+1:]
            seq = "".join(seqTmp.split())
            ofile.write(datum[:desc_end] + "\n" + seq + "\n")