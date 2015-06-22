import sys

# Get longest sequence and put into displayable string
def get_longest(stream):
    stream.seek(0, 0)

    lstring = 'Longest Sequence: \n'

    line = stream.readline()

    maximum = 0

    # FIND MAXIMUM
    while line:
        if line[0] == '>' and maximum < int(line[line.rfind("length=") + 7:-1]):
            maximum = int(line[line.rfind("length=") + 7:-1])
        line = stream.readline()

    # SEEK BEGINNING
    stream.seek(0, 0)

    # GET MORE INFO ON IT
    line = stream.readline()
    while line:
        if line[0] == '>' and int(line[line.rfind("length=") + 7:-1]) == maximum:
            lstring += line
            break
        line = stream.readline()

    return lstring


# Get shortest sequence and put into displayable string
def get_shortest(stream):
    stream.seek(0, 0)

    sstring = 'Shortest Sequence: \n'

    line = stream.readline()

    minimum = sys.maxint

    # FIND MINIMUM
    while line:
        if line[0] == '>' and minimum > int(line[line.rfind("length=") + 7:-1]):
            minimum = int(line[line.rfind("length=") + 7:-1])
        line = stream.readline()

    # SEEK BEGGINING
    stream.seek(0, 0)

    # GET MORE INFO ON IT
    line = stream.readline()
    while line:
        if line[0] == '>' and int(line[line.rfind("length=") + 7:-1]) == minimum:
            sstring += line
            break
        line = stream.readline()

    return sstring


input_file = sys.argv[1]
output_file = sys.argv[2]

longest = ''
shortest = ''



# INPUT
with open(input_file, "r") as stream_in:
    longest = get_longest(stream_in)
    shortest = get_shortest(stream_in)



# OUTPUT
with open(output_file, "w") as stream_out:
    stream_out.write(longest)
    stream_out.write(shortest)
