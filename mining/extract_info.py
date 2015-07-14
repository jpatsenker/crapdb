import os

files = os.listdir("outputs/0j_out/sample")




with open("0j_info_better", "w") as write:
    for f in files:
        my_info = {}
        final = 0
        total = 0
        if f != "empty_file_for_git":
            with open("outputs/0j_out/sample/" + f, "r") as stream:
                info = stream.read()
                info = info.replace("\n", "")
                points = info.split("-")
                for point in points:
                    if point == "":
                        break
                    opair = point.split(",")
                    hello = 0
                    hi = 0
                    try:
                        print opair[0] + " " + opair[1] + "\n"
                        hello=float(opair[0])
                        hi=float(opair[1])
                    except ValueError:
                        print "NO!"
                        exit(1)
                    my_info[hello] = hi
                for q, p in my_info.items():
                    if q > .95:
                        final += p
                    total += p
                write.write(f + ": " + str(final) + "/" + str(total) + "=" + str(float(final)/float(total)) + "\n")
            print "File " + f + "\n"