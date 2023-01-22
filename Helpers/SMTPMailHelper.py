#from smtplib import SMTP
from Props import StaticProps as SP
from Logger import LogManager as LM
#from smtplib import SMTP_SSL
#from email.mime.text import MIMEText
import smtplib, ssl

class SMTPClient(object):


    @staticmethod
    def sendEmail(message):
        subject = "Bilekler-Web-Scraping-ERROR"
        message = """\
        Subject: Bilekler-Web-Scraping-ERROR
        Error Occured On Scraping Process"""

        #content = "Subject: {0} - {1}".format(subject,message)

        myMailAdress = SP.EmailProps.base_email_account
        password = SP.EmailProps.base_email_password
        sendTo = SP.EmailProps.mail_receiver
        mailHost = SP.EmailProps.mail_host
        mailPort = SP.EmailProps.mail_port

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(mailHost, mailPort) as mail:
                #mail.set_debuglevel(1)
                mail.ehlo()
                #mail.starttls(context=context)
                mail.starttls()
                mail.ehlo()
                mail.login(myMailAdress, password)
                mail.sendmail(myMailAdress, sendTo, message)
        except Exception as e:
            LM.LogManager.logMessage("Error Occured While sending Email - Message : " + str(e) , LM.LogType.EXCEPTION);

