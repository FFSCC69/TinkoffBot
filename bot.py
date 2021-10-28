'''main executing script'''
import threading
import time
from pydantic import ValidationError
from requests import RequestException
from src.settings import (
    STRATEGIES,
    ENABLED_DATABASE_LOGS,
    ENABLE_TELEGRAM_MODULE
)
from src.modules.mail_handler import (
    get_strategy_status_from_mail,
    rise_mail_connection
)
from src.modules.tinkoff_api import TinkoffError
from src.modules.tinkoff_highlvl import (
    get_figi_by_ticker,
    create_market_order
)
from src.modules.telegram_module import (
    create_telegram_bot,
    sustain_dedicated_telegram_handler,
    telegram_basic_log,
    telegram_basic_error_log,
    telegram_strategy_alert_log,
    telegram_executed_order_log
)

def create_telegram_bot_thread() -> None:
    '''Handle all incoming messages'''
    thread = threading.Thread(
            target=sustain_dedicated_telegram_handler,
            daemon=True
        )
    thread.name = 'thread telegram bot'
    thread.start()

def handle_strategy_alert(strategy_alert, figi: str, bot) -> None:
    '''Making decisions and catching exceptions'''

    try:
        executed_order = create_market_order(strategy_alert, figi)
    except RequestException as e:
        telegram_basic_error_log(bot, 'requests error')
    except ValidationError as e:
        telegram_basic_error_log(bot, e.json())
        exit()
        #print(e.json())
    except TinkoffError as e:
        telegram_basic_error_log(bot, f'tinkoff got error {e.message}')
        exit()
        #print(e.message)
    except Exception as e:
        telegram_basic_error_log(bot, f'some really unexpectable error: {e}')
        exit()
        #print('some really unexpectable error')
    else:
        telegram_executed_order_log(bot, executed_order)

def create_trading_threads() -> list:
    '''
    Creating and starting trading threads
    Returns list of created threads
    '''
    created_trading_threads = []
    for strategy_name, ticker in STRATEGIES.items():
        thread = threading.Thread(
            target=sustain_trading_thread,
            args=(strategy_name, ticker),
            daemon=True
        )
        thread.name = 'thread ' + strategy_name
        created_trading_threads.append(thread)
        thread.start()
    return created_trading_threads


def sustain_trading_thread(strategy_name: str, ticker: str):
    '''All in-thread actions and logic'''

    mail_connection = rise_mail_connection()
    figi = get_figi_by_ticker(ticker)
    telegram_bot = create_telegram_bot()
    telegram_basic_log(
        telegram_bot,
        f'started {threading.current_thread().getName()}'
    )

    while True:
        time.sleep(1)
        strategy_alert = get_strategy_status_from_mail(strategy_name, mail_connection)
        print(threading.current_thread().name, end=': ')
        if strategy_alert == 'NoMail':
            pass
        elif strategy_alert == 'TooManyMails':
            telegram_basic_error_log(telegram_bot, 'too many mails') # raise mail sequence error
        else:
            #telegram_strategy_alert_log(telegram_bot, strategy_alert)
            handle_strategy_alert(strategy_alert, figi, telegram_bot)

def sustain_main_thread(active_trading_threads: list) -> None:
    '''Look after other threads'''

    telegram_bot = create_telegram_bot()
    active_threads_count_should_be = (
            len(STRATEGIES) +
            int(ENABLED_DATABASE_LOGS is True) +
            int(ENABLE_TELEGRAM_MODULE is True) * 7 + # with 4 workers
            1 # with main thread
        )

    while True:
        time.sleep(0.5)
        active_threads_count = len(threading.enumerate())

        if active_threads_count < active_threads_count_should_be:
            for thread in active_trading_threads:
                if not thread.is_alive():
                    telegram_basic_error_log(telegram_bot, f'{thread.name} is down')
                    break
            break

def main():
    '''
    Creating and watching threads
    Managing telegram bot and database
    '''

    create_telegram_bot_thread()
    active_trading_threads = create_trading_threads()
    sustain_main_thread(active_trading_threads)
    exit()

if __name__ == '__main__':
    main()


# BBG000C0HQ54 ENDP
# BBG000QCW561 VEON
# BBG000BH5LT6 RIG
# BBG00HTN2CQ3 SPCE
# print(tinkoff_api.get_stock_by_ticker('SPCE'))
