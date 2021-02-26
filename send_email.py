import smtplib
from time import time, ctime
import configs.cfg_email as config

'''
    You need to give permission on your email:
In order for this script to work, you must also enable "less secure apps" to access your Gmail account.
As a warning, this is not ideal, and Google does indeed warn against enabling this feature.
Note: I think that you necessarily need to login on the computer, so google can trust on the device.
https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3V5M3YzRUZnMlppc1hGbnRoVXJzSXBzN3d5UXxBQ3Jtc0trUG5EbV9qYUI3NGc3U01XQ3RRMmRZWlNGZjY1Wm1WeEVvVGRnek5KRVFRcXN1dm5OUEg0V2ExQXRtRjhFRHJlUXVQZ2FIanVpMXJDdWdIQ2lHNE5iRThQdGhpWngxbWlnaWdMWXNFNEt5QUVCUXZ6cw&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps
'''

def Send_Email(subject, msg):
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

# subject = f'Testando som... 2... s... som...'
# msg = f'Pimba master 2018 {ctime(time())}'

# send_email(subject, msg)