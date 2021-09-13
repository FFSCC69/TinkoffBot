'''Email Handler'''

import email
import imaplib
import json
from typing import Union
from .. import settings #EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_SERVER, STRATEGY_NAMES


def rise_mail_connection() -> imaplib.IMAP4_SSL:
    '''Open and return connection using config from settings'''
    mail = imaplib.IMAP4_SSL(settings.EMAIL_SERVER)
    mail.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
    return mail


def get_json_from_mail_content(mail_content: str) -> dict:
    '''From mail_content get message and convert it to json'''
    encoded_json_string = mail_content[(mail_content.find('MESSAGE_START') +
                            len('MESSAGE_START')):mail_content.find('MESSAGE_END')]
    encoded_json_string = encoded_json_string.replace('&#34;', '"').replace('=', '') # formating and
    encoded_json_string = encoded_json_string.replace("\r", '').replace("\n", '') # cleaning string
    json_mail_message = json.loads(encoded_json_string)
    return json_mail_message


def get_strategy_status_from_mail_in_json(strategy_name: str) -> Union[dict, str]:
    '''Receiveing mail and output:
    json dict if works fine
    "NoMail" if empty
    "TooManyMails" if lost sequence'''

    mail = rise_mail_connection()
    mail.select('inbox')

    searchable_strategy_name = '"Alert: ' + strategy_name + '"' # special format for mail.search
    status, data = mail.search(None, f'FROM "TradingView" SUBJECT {searchable_strategy_name} UNSEEN')

    mail_ids = []
    for block in data:
        mail_ids += block.split()

    if len(mail_ids) > 1: # how many mails
        return 'TooManyMails'

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_content = message.get_payload()
                return get_json_from_mail_content(mail_content)
    return 'NoMail'
