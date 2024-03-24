from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
from io import StringIO
import smtplib
def send_email_crash_notification(crash_message):
    email = 'your_email@gmail.com'
    send_to_email = 'receipent_email@gmail.com'
    subject = 'Python application CRASHED!'
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    message = crash_message
    msg.attach(MIMEText(message, 'plain'))
    # Send the message via SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
    print('email sent to ' + str(send_to_email))
    return True
try:
    #Your main code will be placed here
    print(1+1)
except Exception as e:
    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)
    logging.error("Exception occurred", exc_info=True)
    send_email_crash_notification(log_stream.getvalue())