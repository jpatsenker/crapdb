import sys
import io
import os
import subprocess
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email import Encoders

def send_email(info, email, files):
	sender = 'noreply@kirschner.med.harvard.edu'
	receivers = email

	message = MIMEMultipart()
	message['Subject'] = "CRAP Score"
	message['From'] = "CRAP DB <noreply@kirschner.med.harvard.edu>"

	body = MIMEText(info)
	message.attach(body)
	
	for f in files or []:
		with open(f, "rb") as fil:
			msg.attach(MIMEApplication(fil.read(), Content_Disposition='attachment; filename="%s"' % basename(f)))
		#endwith
	#endfor

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, receivers, message.as_string)
		print "Successfully sent email"
	except SMTPException:
		print "Error: unable to send email"
	#endtry

#enddef




#launch from main dir

fastaChecker = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl'

input_file = sys.argv[1]
mail_address = sys.argv[2]

checked_file = input_file[:input_file.rfind('.')] + '_checked' + input_file[input_file.rfind('.'):]







#PERFORM A FASTA CHECK
#print '. /opt/lsf/conf/profile.lsf; bsub -q short -K -W 1 -o ' + checked_file + ' -e tmp/errors.txt perl ' + fastaChecker + ' ' + input_file + ' 0'
#sys.exit(0)
process_fastaCheck = subprocess.Popen(['/bin/bash', '-c', './run_with_profile.sh -q short -K -W 1 -o ' + checked_file + ' -e tmp/errors.txt perl ' + fastaChecker +' '+ input_file +' 0'])


process_fastaCheck.wait() #wait for fasta to finish before continuing


#CHECK IF ITS OK TO CONTINUE
with open('tmp/errors.txt', "r") as fastaErrors:
	if fastaErrors.readline():
		fastaErrors.seek(0,0)
		errorStr = fastaErrors.read()
		send_email("Fasta file improperly formatted: \n" + errorStr, mail_address);
		sys.exit(0);
	#endif
#endwith

#CHANGE INTO MINING DIRECTORY
try:
	os.chdir('mining')
except OSError:
	print "Error, couldn't get into directory mining"
	sys.exit(0)


#THE OUTSTRING
outstr = "Fasta is in proper format \n"

#FILES TO BE ATTACHED
outfiles = []


#TOOLS
addLengths = 'add_lengths.py'
getLongShort = 'get_longest_and_shortest.py'
getLenDist = 'get_length_distribution.py'



#ADD LENGTHS TO THE FILE

file_with_lengths = checked_file[:checked_file.rfind('.')] + '_lengths' + checked_file[checked_file.rfind('.'):]

process_addLengths = subprocess.Popen(['/bin/sh', '-c', '../run_with_profile.sh -q short -K -W 1 python ' + addLengths + ' ../' + checked_file + ' ../' + file_with_lengths])
process_addLengths.wait()

#GET LONG AND SHORT SEQS



long_short =  input_file[:input_file.rfind('.')] + '_long_short' + input_file[input_file.rfind('.'):]


process_longShort = subprocess.Popen(['/bin/sh', '-c', '../run_with_profile.sh -q short -K -W 1 python ' + getLongShort + ' ../' + file_with_lengths + ' ../' + long_short])


#GET LENGTH DISTRIBUTION

len_dist = 'tmp' + input_file[input_file.rfind('/'):] + '.hist'

process_lenDistribution = subprocess.Popen(['/bin/sh', '-c', '../run_with_profile.sh -q short -K -W 1 python ' + getLenDist + ' ../' + file_with_lengths + ' ' + len_dist + ' 100'])


#PULLING ANALYSIS

process_longShort.wait()

with open('../' + long_short) as stream_long_short:
	outstr += '\n' + stream_long_short.read()
#endwith


process_lenDistribution.wait()
outfiles.append(len_dist + '.png')



#SEND EMAIL WITH RESULTS
send_email(outstr, mail_address, outfiles)