'''main executing file'''
import os
import json
import requests, socket
from pydantic import ValidationError
from src.settings import (
    STRATEGY_NAMES
)
from src.modules import tinkoff_api, tinkoff_classes
from src.modules.mail_handler import get_strategy_status_from_mail
from src.modules.tinkoff_highlvl import * # to do

def main():
    try:
        for strategy_name in STRATEGY_NAMES:
            print(get_strategy_status_from_mail(strategy_name))
    except socket.error as e:
        print(e)
        print('socket error')

    try:
        resp_base = tinkoff_api.get_orders()
        print(type(resp_base))
        print(resp_base)
    except requests.RequestException as e:
        print(e)
        print('requests error')
    except tinkoff_api.TinkoffError as e:
        print(type(e))
        print(e.tracking_id)
    except ValidationError as e:
        print(e.json())
        print('validation error')


if __name__ == '__main__':
    main()


'''
def func():
    return request.get(url).json()

t1 = Thread(target = func)
t2 = Thread(target = func)

t1.start()
t2.start()

while True:
    pass
'''
