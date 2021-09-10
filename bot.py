'''main file'''
import os
import tinvest
from src import settings
from src.modules import mail_handler

mail_handler.test_mail()





'''c = tinvest.SyncClient(settings.TINKOFF_API_TOKEN) # для брокерского счета
r = c.get_portfolio() # если портфелей несколько, то их нужно указать'''
