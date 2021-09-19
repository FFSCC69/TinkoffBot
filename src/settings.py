'''Keys, tokens and configs'''

import os


TINKOFF_API_TOKEN = os.getenv('TINKOFF_API_TOKEN')
#TINKOFF_API_TOKEN = 'your_token'
'''Token from tinkoff'''

TINKOFF_IIS_ID = os.getenv('TINKOFF_IIS_ID')
#TINKOFF_IIS_ID = 'your_tinkoffiis_id'
'''Iis broker account id'''

TINKOFF_ID = os.getenv('TINKOFF_ID')
#TINKOFF_ID = 'your_tinkoff_id'
'''Default broker account id'''

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
#EMAIL_ADDRESS = 'your_email_address'
'''Mail address'''

EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
#EMAIL_PASSWORD = 'your_email_password'
'''Mail password'''

EMAIL_SERVER = os.getenv('EMAIL_SERVER')
#EMAIL_SERVER = 'your_email_server'
'''Mail server'''

TIME_ZONE_UTC = 'UTC'
TIME_ZONE_LOCAL = os.getenv('TIME_ZONE_LOCAL')
#TIME_ZONE = 'your_time_zone'
'''Time zones'''

STRATEGY_NAMES = (
  "BTC_TEST_ALERT",
)
'''List of strategies'''
