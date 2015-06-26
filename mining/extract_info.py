import os

files = os.listdir("outputs/0j_out/sample")




with open("0j_info_better", "w") as write:
    for f in files:
        my_info = {}
        final = 0
        sum = 0
        if f != "empty_file_for_git":
            with open("outputs/0j_out/sample/" + f, "r") as stream:
                info = stream.read()
                points = info.split("-")
                for point in points:
                    opair = point.split(",")
                    try:
                        x=float(opair[0])
                        y=float(opair[1])
                    except ValueError:
                        print "NO!"
                        exit(1)
                    my_info[x] = y
                for q, p in my_info.items():
                    if q > .95:
                        final += p
                    sum += p
                write.write(f + ": " + final + "/" + sum + "=" + float(final)/float(sum) + "\n")
            print "File " + f + "\n"