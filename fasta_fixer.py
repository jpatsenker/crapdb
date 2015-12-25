import shutil
def fix_file(input_file, output_file):
    with open(input_file, "r") as ifile:
        everything = ifile.read()
    with open(output_file, "w") as ofile:
        yes = True
        for line in everything.split("\n"):
            try:
                if line[0] == ">":
                    if yes:
                        yes = False
                    else:
                        ofile.write("\n")
                    ofile.write(line + "\n")
                else:
                    ofile.write(line)
            except IndexError:
                pass