from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(info, email, files):
    sender = 'noreply@kirschner.med.harvard.edu'
    receivers = email

    message = MIMEMultipart(
        From="CRAP DB <noreply@kirschner.med.harvard.edu>",
        Subject="CRAP Score"
    )

    body = MIMEText(info)
    message.attach(body)

    for f in files or []:
        with open(f, "rb") as fil:
            attach_file = MIMEApplication(fil.read())
            attach_file.add_header('Content-Disposition', 'attachment', filename=f)
            message.attach(attach_file)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"
