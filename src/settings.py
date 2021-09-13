'''Keys, tokens and configs'''

import os


TINKOFF_API_TOKEN = os.getenv('TINKOFF_API_TOKEN')
#TINKOFF_API_TOKEN = 'your_token'
'''Token from tinkoff'''

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
#EMAIL_ADDRESS = 'your_email_address'
'''Mail address'''

EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
#EMAIL_PASSWORD = 'your_email_password'
'''Mail password'''

EMAIL_SERVER = os.getenv('EMAIL_SERVER')
#EMAIL_SERVER = 'your_email_server'
'''Mail server'''

STRATEGY_NAMES = (
  "BTC_TEST_ALERT",
)


