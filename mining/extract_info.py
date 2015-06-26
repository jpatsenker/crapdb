import os

files = os.listdir("outputs/0j_out/sample")

with open("0j_info", "w") as write:
    for f in files:
        if f != "empty_file_for_git":
            with open("outputs/0j_out/sample/" + f, "r") as stream:
                info = stream.read()
                try:
                    val = int(info[info.find(".95,")+4:info.find("-",info.find(".95,"))])
                    write.write(f[0:5] + ": " + str(val) + "\n")
                except ValueError:
                    print "NO!"
                    exit(1)
            print "File " + f + "\n"