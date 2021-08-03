#!/usr/bin/env python3

from email.message import EmailMessage
import smtplib
import getpass

message = EmailMessage()

sender = 'me@example.com'
recipient = 'you@example.com'

message['From'] = sender
message['To'] = recipient

message['Subject'] = 'email subject'

body = '''email body
bla bla
text
bla
Regards,
signature.
'''
message.set_content(body)

# View the email being sent
print(message)

mail_server = smtplib.SMTP_SSL('smtp.gmail.com')  # smtp server address

# If you want to see the SMTP messages that are
# being sent back and forth by the smtplib module behind the scenes,
# you can set the debug level on the SMTP or SMTP_SSL object.
mail_server.set_debuglevel(1)

mail_pass = getpass.getpass('Password? ')  # sender's email password

mail_server.login(sender, mail_pass)
mail_server.send_message(message)

mail_server.quit()


