import sys
import os
import io


#Get longest sequence and put into displayable string
def get_longest(stream):
	
	stream.seek(0,0)
	
	lstring = 'Longest: '

	line = stream.readline()

	max = 0
	
	#FIND MAXIMUM
	while line:
		if line[0] == '>' and max < line[line.rfind("length=")+7:]:
			max = line[line.rfind("length=")+7:]
			print max
		#endif
		line = stream.readline()
	#endwhile

	#SEEK BEGGINING
	stream.seek(0,0)
	
	#GET MORE INFO ON IT
	line = stream.readline()
	while line:
		if line[line.rfind("length=")+7:] == max :
			lstring += line
			break
		#endif
		line = stream.readline()
	#endwhile

	return lstring
#enddef

#Get shortest sequence and put into displayable string
def get_shortest(stream):
	
	stream.seek(0,0)
	
	sstring = 'Shortest: '
	
	line = stream.readline()
	
	min = sys.maxint
	
	#FIND MINIMUM
	while line:
		if line[0] == '>' and min > line[line.rfind("length=")+7:]:
			min = line[line.rfind("length=")+7:]
			print min
		#endif
		line = stream.readline()
	#endwhile
	
	#SEEK BEGGINING
	stream.seek(0,0)
	
	#GET MORE INFO ON IT
	line = stream.readline()
	while line:
		if line[line.rfind("length=")+7:] == min :
			lstring += line
			break
		#endif
		line = stream.readline()
	#endwhile

	return sstring
#enddef




input_file = sys.argv[1]
output_file = sys.argv[2]

longest = ''
shortest = ''



#INPUT
with open(input_file, "r") as stream_in:
	longest = get_longest(stream_in)
	shortest = get_shortest(stream_in)
#endwith



#OUTPUT
with open(output_file, "w") as stream_out:
	stream_out.write(longest)
	stream_out.write(shortest)
#endwith