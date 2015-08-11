def fix_file(input_file):
    with open(input_file, "r") as ifile:
        everything = ifile.read()
    with open(input_file, "w") as ofile:
        for line in everything.split("\n"):
            if line[0] == ">":
                ofile.write("\n" + line + "\n")
            else:
                ofile.write(line)