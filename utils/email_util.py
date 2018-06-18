from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from myspiders import settings
import logging
import traceback
import time, random


def send_email(subject, content, receivers):
    message = MIMEText(content, 'html')
    message['From'] = 'robot@lamudatech.com'
    message['Subject'] = Header(subject, 'utf-8')
    index = random.randint(0, len(settings.SENDER)-1)
    try:
        smtp = SMTP_SSL(settings.HOST_SERVER)
        smtp.ehlo(settings.HOST_SERVER)
        smtp.login(settings.SENDER[index], settings.PWD[index])
        smtp.sendmail(settings.SENDER[index], list(receivers), message.as_string())
        smtp.quit()
        logging.info('success')
    except:
        logging.error(traceback.print_exc())
        time.sleep(5)
