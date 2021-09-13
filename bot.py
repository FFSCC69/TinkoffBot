'''main file'''
import os
import json
import requests
from pydantic import BaseModel, Field, ValidationError
from src import settings
from src.modules import mail_handler, tinkoff_api

for strategy_name in settings.STRATEGY_NAMES:
    print(mail_handler.get_strategy_status_from_mail_in_json(strategy_name))

#print(json.dumps(tinkoff_api.get_portfolio(), ensure_ascii=False, sort_keys=True, indent=4))

#print(json.dumps(tinkoff_api.get_user_accounts(), ensure_ascii=False, sort_keys=True, indent=2))

#print(tinkoff_api.generate_request('user/accounts'))

'''resp = tinkoff_api.UserResponse()
for account in tinkoff_api.UserResponse.payload.UserAccounts:
    print(account.broker_account_type)
print(json.dumps(res))'''
try:
    account_list = tinkoff_api.get_user_accounts()
except ValidationError as e:
    print(e.json())

print(type(account_list))
for account in account_list:
    print(account.broker_account_id)