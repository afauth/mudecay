import smtplib
import cfg_email as cfg

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(cfg.EMAIL_ADDRESS, cfg.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(from_addr=cfg.EMAIL_ADDRESS, to_addrs=cfg.EMAIL_ADDRESS, msg=message)
        server.quit()
        print('Success: Email sent.')
    except:
        print('Email failed to send.')

subject = 'Testando som... 2... s... som...'
msg = 'Pimba master 2018'

send_email(subject, msg)