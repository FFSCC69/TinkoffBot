'''All functions for tinkoff API'''

import requests, json
from typing import Optional, List
from pydantic import BaseModel, Field
from .. import settings

API = 'https://api-invest.tinkoff.ru/openapi/'
HEADERS = {"Authorization": f'Bearer {settings.TINKOFF_API_TOKEN}'}



class UserAccount(BaseModel):
    broker_account_id: str = Field(alias='brokerAccountId')
    broker_account_type: str = Field(alias='brokerAccountType')

class UserAccounts(BaseModel):
    accounts: List[UserAccount]

class TinkoffBaseResponse(BaseModel):
    '''Base response model'''
    tracking_id: str = Field(alias='trackingId')
    status: str

class PortfolioResponse(TinkoffBaseResponse):
    ''''''
    payload: str

class MarketResponse(TinkoffBaseResponse):
    ''''''
    payload: str

class OperationsResponse(TinkoffBaseResponse):
    ''''''
    payload: str

class UserResponse(TinkoffBaseResponse):
    '''response model for 
    user/accounts'''
    payload: UserAccounts



def generate_request(endpoint: str, params: Optional[dict] = None) -> dict:
    '''Generates request using endpoint and params
    returns str in json format'''
    a = json.dumps(requests.get(API + endpoint, headers=HEADERS, params=params).json())
    print(type(a))
    print(a)
    return a


def get_portfolio(brocker_id: Optional[str] = None) -> json:
    '''Get portfolio in json'''
    if brocker_id:
        brocker_id = {"brokerAccountId": brocker_id}
    return generate_request("portfolio", brocker_id)

def get_sub(sub, params) -> str:
    '''For tests'''

    return generate_request(sub)

def get_user_accounts() -> UserAccounts:
    return UserResponse.parse_raw(generate_request('user/accounts')).payload.accounts

def get_user_accounts_old() -> str:
    '''all user accounts'''
    return generate_request("user")
