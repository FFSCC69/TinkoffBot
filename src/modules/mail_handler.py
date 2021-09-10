'''Email Handler'''

import email
import imaplib
from .. import settings #EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_SERVER

def test_mail():
    '''receiveing mail and output json'''
    # connect to the mail server and go to its inbox
    mail = imaplib.IMAP4_SSL(settings.EMAIL_SERVER)
    mail.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)

    subject_to_search = '"Alert: BTC_TEST_ALERT"' #TEMP

    mail.select('inbox')
    status, data = mail.search(None, f'FROM "TradingView" SUBJECT {subject_to_search} UNSEEN')
    mail_ids = []
    for block in data:
        mail_ids += block.split()
    print(len(mail_ids))
    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_content = message.get_payload()
                encoded_json = mail_content[mail_content.find('MESSAGE_START') + len ('MESSAGE_START'):mail_content.find('MESSAGE_END')]
                encoded_json = encoded_json.replace('&#34;', '"').replace('=', '').replace("\r", '').replace("\n", '')
                print(encoded_json)
