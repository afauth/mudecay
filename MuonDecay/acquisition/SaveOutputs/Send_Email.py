import smtplib
from time import time, ctime
try:
    from acquisition.Configs import cfg_email
except:
    print('\nNo config file for the email.\n'+
    'Please, make sure you have a config-file named "cfg_email.py" and with the following files:\n'+
    'EMAIL_ADDRESS, EMAIL_DESTINATION and PASSWORD --- all in the Config folder.\n\n')
    raise

'''
    You need to give permission on your email:
In order for this script to work, you must also enable "less secure apps" to access your Gmail account.
As a warning, this is not ideal, and Google does indeed warn against enabling this feature.
Note: I think that you necessarily need to login on the computer, so google can trust on the device.
https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3V5M3YzRUZnMlppc1hGbnRoVXJzSXBzN3d5UXxBQ3Jtc0trUG5EbV9qYUI3NGc3U01XQ3RRMmRZWlNGZjY1Wm1WeEVvVGRnek5KRVFRcXN1dm5OUEg0V2ExQXRtRjhFRHJlUXVQZ2FIanVpMXJDdWdIQ2lHNE5iRThQdGhpWngxbWlnaWdMWXNFNEt5QUVCUXZ6cw&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps
'''



def SendEmail(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(cfg_email.EMAIL_ADDRESS, cfg_email.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(from_addr=cfg_email.EMAIL_ADDRESS, to_addrs=cfg_email.EMAIL_DESTINATION, msg=message)
        server.quit()
        print('Success: Email sent.\n\n\n')
    except:
        print('Email failed to send.\n\n\n')
