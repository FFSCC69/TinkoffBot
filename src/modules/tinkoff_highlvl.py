'''High lvl functions fot tinkoff API'''

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

from .tinkoff_api import (
    get_stock_by_ticker,
    post_limit_order,
    post_market_order
)


def get_figi_by_ticker(ticker: str) -> str:
    '''Figi in str for exact ticker'''
    return get_stock_by_ticker(ticker)[0].figi

def create_market_order(strategy_alert, figi: str) -> PlacedMarketOrder:
    '''Execute strategy using market order'''
    return post_market_order(
        MarketOrderRequest.parse_obj(
            {
                'lots': 0,
                'operation': strategy_alert.order_action.capitalize()
            }
        ),
        figi
    )
