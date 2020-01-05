#!/usr/bin/env python3

from os.path import dirname, realpath, join
from email.mime.text import MIMEText
import base64
import smtplib
from string import printable


def create_email(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
    Returns:
      An object containing a base64url encoded email object.
    """
    # This is intended to strip non-ascii chars in message_text
    message_text = ''.join(filter(lambda x: x in printable, message_text))
    
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return message.as_bytes()


def default_gmail_credential_path():
    return join(dirname(realpath(__file__)), 'gmail_credentials.txt')


def send_email(message, subject='', to=None, gmail_credential_file=None):
    # See: https://support.google.com/accounts/answer/185833
    # for how to generate "App Passwords", for offline access to gmail account
    # (service accounts can't really be used with non-GSuit (i.e. personal)
    # gmail accounts)
    if gmail_credential_file is None:
        gmail_credential_file = default_gmail_credential_path()

    with open(gmail_credential_file, 'r') as f:
        lines = [x for x in [x.strip() for x in f.readlines()] if x]
    assert len(lines) == 2, f'got {len(lines)} lines, but expected 2'
    gmail_acc, gmail_passw = lines
    if '@' not in gmail_acc:
        gmail_acc += '@gmail.com'

    # Send to yourself by default.
    if to is None:
        to = gmail_acc

    # To remove non-ascii characters, since their presence seem to make the 
    # try block fail somewhere.

    email = create_email(gmail_acc, to, subject, message)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_acc, gmail_passw)
        server.sendmail(gmail_acc, to, email)
        server.close()
        #print('Email sent!')
    except Exception as err:
        print('Something went wrong...')
        print(err)
        #import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    subject = 'Test subject'
    message = 'Testing testing 123'
    send_email(message, subject=subject)

