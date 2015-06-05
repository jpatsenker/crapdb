import sys
import io
import os
import subprocess
import smtplib

def send_email(info, email):
	sender = 'noreply@kirschner.med.harvard.edu'
	receivers = email

	message = "From: CRAP DB <noreply@kirschner.med.harvard.edu> "+'\n' + "Subject: CRAP Score" + '\n' + info

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, receivers, message)
		print "Successfully sent email"
	except SMTPException:
		print "Error: unable to send email"
	#endtry

#enddef




#launch from main dir

fastaChecker = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl';

input_file = "mining/" + sys.argv[1]
mail_address = sys.argv[2]

checked_file = input_file[:input_file.rfind('.')] + '_checked' + input_file[input_file.rfind('.'):]


#MAKE LSF PROFILE FOR ORCHESTRA
#process_makeProf = subprocess.Popen('./opt/lsf/conf/profile.lsf');

#process_makeProf.wait()


#PERFORM A FASTA CHECK
print 'bsub -q short -K -W 1 -o ' + checked_file + ' -e tmp/errors.txt perl ' + fastaChecker + ' ' + input_file + ' 0'
sys.exit(0)
process_fastaCheck = subprocess.Popen('bsub -q short -K -W 1 -o ' + checked_file + ' -e tmp/errors.txt perl ' + fastaChecker + ' ' + input_file + ' 0')


process_fastaCheck.wait() #wait for fasta to finish before continuing


#CHECK IF ITS OK TO CONTINUE
with open('tmp/errors.txt') as fastaErrors:
	if fastaErrors.readline():
		fastaErrors.seek(0,0)
		errorStr = fastaErrors.read()
		send_email("Fasta file improperly formatted: \n" + errorStr, mail_address);
		sys.exit(0);
	#endif
#endwith


#ADD LENGTHS TO THE FILE

file_with_lengths = checked_file[:input_file.rfind('.')] + '_lengths' + checked_file[input_file.rfind('.'):]




outstr = "Fasta is in proper format"


#SEND EMAIL WITH RESULTS
send_email(outstr, mail_address)