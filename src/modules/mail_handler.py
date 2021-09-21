'''Email Handler module'''

import email
import imaplib
import json
from typing import Union
from decimal import Decimal
from pydantic import BaseModel
from ..settings import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    EMAIL_SERVER
)

class StrategyAlert(BaseModel):
    '''Strategy alert object'''
    ticker: str
    order_action: str
    quantity: int
    price: Decimal
    position: int
    market_position: str
    time: str

def rise_mail_connection() -> imaplib.IMAP4_SSL:
    '''Open and return connection using config from settings'''
    mail = imaplib.IMAP4_SSL(EMAIL_SERVER)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    return mail

def get_strategy_alert_mail_content(mail_content: str) -> StrategyAlert:
    '''From mail_content get message and convert it to json'''
    mail_content = mail_content.replace(
        "\r", ''
    ).replace(
        "\n", ''
    ).replace(
        '=', ''
    )

    encoded_json_string = mail_content[
        (mail_content.find('MESSAGE_START') +
            len('MESSAGE_START')):mail_content.find('MESSAGE_END')
    ]

    encoded_json_string = encoded_json_string.replace('&#34;', '"')

    strategy_alert = StrategyAlert.parse_raw(encoded_json_string)
    return strategy_alert

def get_strategy_status_from_mail(strategy_name: str) -> Union[StrategyAlert, str]:
    '''
    Receiveing mail and output:
    StrategyAlert object if works fine
    "NoMail" if empty mail list
    "TooManyMails" if lost sequence
    '''

    mail = rise_mail_connection()
    mail.select('inbox')

    searchable_strategy_name = (
        '"Alert: ' + strategy_name + '"'
    ) # special format for mail.search

    status, data = mail.search(
        None,
        f'FROM "TradingView" SUBJECT {searchable_strategy_name} UNSEEN'
    )

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
                return get_strategy_alert_mail_content(mail_content)
    return 'NoMail'
