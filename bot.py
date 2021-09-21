'''main executing file'''
import threading
import time
from pydantic import ValidationError
from src.settings import (
    STRATEGY_NAMES
)
from src.modules import tinkoff_api, tinkoff_classes
from src.modules.mail_handler import get_strategy_status_from_mail
from src.modules.tinkoff_highlvl import * # to do

def sustain_trading_thread(strategy_name: str):
    '''All in-thread actions and logic'''
    while True:
        time.sleep(1)
        strategy_alert = get_strategy_status_from_mail(strategy_name)
        if strategy_alert == 'NoMail':
            pass
        elif strategy_alert == 'TooManyMails':
            pass #raise mail sequence error
        else:
            #print logs
            print('got order')
            executed_order = tinkoff_api.post_market_order(
                tinkoff_classes.MarketOrderRequest.parse_obj(
                    {
                        'lots': strategy_alert.quantity,
                        'operation': strategy_alert.order_action.capitalize()
                    }
                ),
                'BBG000C0HQ54')
            #executed logs

def main():
    trading_threads = []
    for strategy_name in STRATEGY_NAMES:
        thread = threading.Thread(
        target=sustain_trading_thread,
        args=(strategy_name,),
        daemon=True
        )
        thread.name = 'thread ' + strategy_name
        trading_threads.append(thread)
        thread.start()

    while True:
        time.sleep(0.5)
        active_threads_count = len(threading.enumerate())
        if active_threads_count < len(STRATEGY_NAMES) + 1: #with main thread
            for thread in trading_threads:
                if not thread.is_alive():
                    break #logs
            break


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
# BBG000C0HQ54 ENDP
# BBG000QCW561 VEON
