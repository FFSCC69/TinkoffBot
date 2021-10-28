'''Basic functions for tinkoff API'''

import json
from typing import Optional, Union
import requests
from ..settings import (
    TINKOFF_API_TOKEN,
    TINKOFF_IIS_ID,
    TINKOFF_ID
)
from pydantic import BaseModel
from .tinkoff_classes import (
    TinkoffBaseResponse,
    TinkoffErrorObject,
    Empty,
    MoneyAmount,
    Order,
    OrdersResponse,
    LimitOrderRequest,
    PlacedLimitOrder,
    LimitOrderResponse,
    MarketOrderRequest,
    PlacedMarketOrder,
    MarketOrderResponse,
    Position,
    Portfolio,
    PortfolioResponse,
    CurrencyPosition,
    Currencies,
    PortfolioCurrenciesResponse,
    OrderResponse,
    OrderBook,
    OrderbookResponse,
    SearchMarketInstrument,
    SearchMarketInstumentResponse,
    MarketInstrument,
    MarketInstrumentList,
    MarketInstrumentListResponse,
    OperationsResponse,
    Operations,
    Operation,
    UserAccount,
    UserAccounts,
    UserAccountsResponse
)

API = 'https://api-invest.tinkoff.ru/openapi/'
HEADERS = {'Authorization': f'Bearer {TINKOFF_API_TOKEN}'}

class TinkoffError(Exception):
    '''Base class for Tinkoff exception'''
    def __init__(self, TinkoffErrorObject):
        self.tracking_id = TinkoffErrorObject.tracking_id
        self.message = TinkoffErrorObject.payload.message
        self.code = TinkoffErrorObject.payload.code

def observe_tinkoff_exception(response_json: str): # for testing purpose
    '''Raise exception if tinkoff server cannot handle request
    Has tracking_id, message, code'''
    examinated_response_object = TinkoffBaseResponse.parse_raw(response_json)
    if examinated_response_object.status == 'Error':
        error_object = TinkoffErrorObject.parse_raw(response_json)
        print(error_object)
        raise TinkoffError(error_object)

def setup_broker_id(
    broker_id: Optional[str] = None
) -> Union[None, str]:
    '''Setting broker account param for work'''
    if broker_id == 'TinkoffIis':
        broker_id = {'brokerAccountId': TINKOFF_IIS_ID}
    if broker_id == 'Tinkoff':
        broker_id = {'brokerAccountId': TINKOFF_ID}
    return broker_id

def send_get_request(
    endpoint: str,
    params: Optional[dict] = None
) -> str:
    '''using endpoint for api and params returns response str in json format'''
    return json.dumps(
        requests.get(
            API + endpoint,
            headers=HEADERS,
            params=params
        ).json()
    )

def send_post_request(
    endpoint: str,
    body: Optional[dict] = None,
    params: Optional[dict] = None
) -> str:
    '''using endpoint for api, body and params returns response str in json format'''
    return json.dumps(
        requests.post(
            API + endpoint,
            data=json.dumps(body),
            headers=HEADERS,
            params=params
        ).json()
    )

def get_orders(
    broker_id: Optional[str] = None
) -> list[Order]:
    '''
    All active orders as list
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/orders/get_orders
    '''
    response_json = send_get_request(
        'orders',
        setup_broker_id(broker_id)
    )
    observe_tinkoff_exception(response_json)
    return OrdersResponse.parse_raw(
        response_json
    ).payload

def post_limit_order(
    body: LimitOrderRequest,
    figi: str,
    broker_id: Optional[str] = None
) -> PlacedLimitOrder:
    '''
    Post limit order and returns response as object
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/orders/post_orders_limit_order
    '''
    params = {'figi': figi}
    if broker_id:
        params.update(setup_broker_id(broker_id))

    response_json = send_post_request(
        'orders/limit-order',
        body=json.loads(body.json()), #{'lots': 1, 'operation': 'Sell', 'price': 1.5}
        params=params
    )
    observe_tinkoff_exception(response_json)
    return LimitOrderResponse.parse_raw(
        response_json
    ).payload

def post_market_order(
    body: MarketOrderRequest,
    figi: str,
    broker_id: Optional[str] = None
) -> PlacedMarketOrder:
    '''
    Post market order and returns response as object
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/orders/post_orders_market_order
    '''

    params = {'figi': figi}
    if broker_id:
        params.update(setup_broker_id(broker_id))

    response_json = send_post_request(
        'orders/market-order',
        body=json.loads(body.json()), #{'lots': 1, 'operation': 'Sell'}
        params=params
    )
    observe_tinkoff_exception(response_json)
    return MarketOrderResponse.parse_raw(
        response_json
    ).payload

def post_order_cancel(
    order_id: str,
    broker_id: Optional[str] = None
) -> Empty:
    '''
    Cancel order by id and returns Empty object
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/orders/post_orders_cancel
    '''
    params = {'orderId': order_id}
    if broker_id:
        params.update(setup_broker_id(broker_id))

    response_json = send_post_request(
        'orders/cancel',
        params=params
    )
    observe_tinkoff_exception(response_json)
    return Empty.parse_raw(
        response_json
    )

def get_portfolio(
    broker_id: Optional[str] = None
) -> Portfolio:
    '''
    All active positions as list
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/portfolio/get_portfolio
    '''
    response_json = send_get_request(
        'portfolio',
        params=setup_broker_id(broker_id)
    )
    observe_tinkoff_exception(response_json)
    return PortfolioResponse.parse_raw(
        response_json
    ).payload.positions

def get_portfolio_currencies(
    broker_id: Optional[str] = None
) -> Currencies:
    '''
    All currencies balances as list
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/portfolio/get_portfolio_currencies
    '''
    response_json = send_get_request(
        'portfolio/currencies',
        params=setup_broker_id(broker_id)
    )
    observe_tinkoff_exception(response_json)
    return PortfolioCurrenciesResponse.parse_raw(
        response_json
    ).payload.currencies

def get_orderbook(
    figi: str,
    depth: int
) -> OrderBook:
    '''
    Orderbook container with 2 lists "asks" and "bids" with objects (ammount = depth <20)
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/market/get_market_orderbook
    '''
    response_json = send_get_request(
        'market/orderbook',
        params={'figi': figi, 'depth': depth}
    )
    observe_tinkoff_exception(response_json)
    return OrderbookResponse.parse_raw(
        response_json
    ).payload

def get_stock_by_figi(
    figi: str
) -> SearchMarketInstrument:
    '''
    Found result for figi as object
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/market/get_market_search_by_figi
    '''
    response_json = send_get_request(
        'market/search/by-figi',
        params={'figi': figi}
    )
    observe_tinkoff_exception(response_json)
    return SearchMarketInstumentResponse.parse_raw(
        response_json
    ).payload

def get_stock_by_ticker(
    ticker: str
) -> MarketInstrumentList:
    '''
    All found results for ticker as list
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/market/get_market_search_by_ticker
    '''
    response_json = send_get_request(
        'market/search/by-ticker',
        params={'ticker': ticker}
    )
    observe_tinkoff_exception(response_json)
    return MarketInstrumentListResponse.parse_raw(
        response_json
    ).payload.instruments

def get_operations(
    from_date: str = '2015-12-31T00:00:00+00:00',
    to_date: str = '3015-12-31T00:00:00+00:00',
    figi: Optional[str] = None,
    broker_id: Optional[str] = None
) -> Operations:
    '''
    Returns all operations in date range filtered by figi as list
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/operations/get_operations
    '''
    params = {'from': from_date, 'to': to_date}
    if broker_id:
        params.update(setup_broker_id(broker_id))
    if figi:
        params.update({'figi': figi})

    response_json = send_get_request(
        '/operations',
        params=params
    )
    observe_tinkoff_exception(response_json)
    return OperationsResponse.parse_raw(
        response_json
    ).payload.operations

def get_user_accounts() -> UserAccounts:
    '''
    Returns all trading accounts as list
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/user/get_user_accounts
    '''
    response_json = send_get_request(
            'user/accounts'
        )
    observe_tinkoff_exception(response_json)
    return UserAccountsResponse.parse_raw(
        response_json
    ).payload.accounts
