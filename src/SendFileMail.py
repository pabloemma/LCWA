'''
Created on Apr 26, 2020

@author: klein
'''


    
    
from socket import gethostname
import smtplib
    #import email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
import os


import json




class MyMail(object):
    '''
    sends file by email
    '''


    def __init__(self,file,recipients,subject=None, message =None):
        '''
        Constructor
        '''
        self.file = file # list of files to be sent
        self.recipients = recipients
        self.subject=subject
        self.mess=message
        
        
    def send_email_pdf_figs(self, pimp=None):
    ## credits: http://linuxcursor.com/python-programming/06-how-to-send-pdf-ppt-attachment-with-html-body-in-python-script
        with open(pimp,'r')as f:
            a=f.readline().split()
            
            
           
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(a[0], a[1])
        # Craft message (obj)
        msg = MIMEMultipart()

        message = self.mess
        msg['Subject'] = self.subject
        msg['From'] = 'pabloemma@gmail.com'
        msg['To'] = self.recipients
        # Insert the text to the msg going by e-mail
        msg.attach(MIMEText(message, "plain"))
        # Attach the pdf to the msg going by e-mail
        with open(self.file, "rb") as f:
            #attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(self.file))
        msg.attach(attach)
        # send msg
        server.send_message(msg)
            
if __name__ == '__main__':
    
    file='/Users/klein/scratch/LCWA_TOTAL_2020-04-26speedfile.pdf'
    recipients='pabloemma@casitadongaspar.com, pabloemma@gmail.com'
    message =' this is the LCWA file '
    subject = 'pdf file'
    impo_file = '/Users/klein/private/LCWA/andifile'
    MM=MyMail(file,recipients,subject,message)
    MM.send_email_pdf_figs(impo_file)
    
