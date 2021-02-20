import smtplib
from time import time, ctime
import configs.cfg_email as config

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(from_addr=config.EMAIL_ADDRESS, to_addrs=config.EMAIL_DESTINATION, msg=message)
        server.quit()
        print('Success: Email sent.')
    except:
        print('Email failed to send.')

subject = f'Testando som... 2... s... som...'
msg = f'Pimba master 2018 {ctime(time())}'

send_email(subject, msg)