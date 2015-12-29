import shutil
def fix_file(input_file, output_file):
    with open(input_file, "r") as ifile:
        everything = ifile.read()
    with open(output_file, "w") as ofile:
        for datum in everything.split(">"):
            ofile.write(">")
            seq_start = datum.find("\n")
            while datum[seq_start].isspace():
                seq_start+=1
            seqTmp = datum[seq_start+1:]
            seq = "".join(seqTmp.split())
            ofile.write(datum[:seq_start] + "\n" + seq + "\n")