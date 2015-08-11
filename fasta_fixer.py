import shutil
def fix_file(input_file):
    with open(input_file, "r") as ifile:
        everything = ifile.read()
    with open(input_file + ".tmp", "w") as ofile:
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
    shutil.move(input_file + ".tmp", input_file)