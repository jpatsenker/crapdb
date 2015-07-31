

f = "genomes/CELEGcurnt.longest.fa"

final_proteins = {}


with open(f, "r") as in_stream:
    everything = in_stream.read()
    proteins = everything.split(">")
    proteins = proteins[1:]
    for protein in proteins:
        sequence = protein[protein.find("\n")+1:]
        descrip = protein[:protein.find("\n")]
        sequence = sequence.replace("\n", "")
        descrip_arr = descrip.split("\t")

        if descrip_arr[2] in final_proteins:
            if len(sequence) > len(final_proteins[descrip_arr[2]]):
                final_proteins[descrip_arr[2]] = sequence
        else:
            final_proteins[descrip_arr[2]] = sequence


with open(f, "w") as out_stream:
    for prot in final_proteins:
        out_stream.write(">" + prot + "\n" + final_proteins[prot] + "\n")