'''Logging and managing trading bot using telegram bot'''

from telegram import (
    Update,
    Bot
)
from telegram.ext import (
    CallbackContext,
    Updater,
    Filters,
    MessageHandler,
)
from ..settings import (
    TELEGRAM_API_TOKEN,
    TELEGRAM_ADMIN_ID
)
from .mail_handler import StrategyAlert

TELEGRAM_ADMIN_ID = int(TELEGRAM_ADMIN_ID)

def dummy_message_handler(update: Update, context: CallbackContext) -> None:
    '''dummy for handlig all messages'''
    if update.message.chat_id == TELEGRAM_ADMIN_ID:
        update.message.reply_text(
            text='okey-dokey'
        )
    else:
        update.message.reply_text(
            text='Access denied'
        )

def sustain_dedicated_telegram_handler():
    '''handler for all incoming messages'''
    updater = Updater(
        token=TELEGRAM_API_TOKEN,
        use_context=True
    )
    updater.dispatcher.add_handler(
        MessageHandler(
            filters=Filters.all,
            callback=dummy_message_handler
        )
    )
    updater.start_polling(poll_interval=0.5)

def create_telegram_bot() -> Bot:
    '''Creating bot object'''
    return Bot(TELEGRAM_API_TOKEN)

def telegram_basic_log(bot: Bot, message: str) -> None: # for testing purpose
    '''Send message to admin'''
    bot.send_message(TELEGRAM_ADMIN_ID, message, disable_notification=True)

def telegram_basic_error_log(bot: Bot, error) -> None:
    '''Send default error message'''
    bot.send_message(TELEGRAM_ADMIN_ID, error)

def telegram_strategy_alert_log(bot: Bot, strategy_alert: StrategyAlert) -> None:
    '''Send strategy alert data'''
    bot.send_message(
        TELEGRAM_ADMIN_ID,
        strategy_alert.json(),
        disable_notification=True
    )

def telegram_executed_order_log(bot: Bot, executed_order) -> None:
    '''Send executed order information'''
    bot.send_message(
        TELEGRAM_ADMIN_ID,
        executed_order
    )
