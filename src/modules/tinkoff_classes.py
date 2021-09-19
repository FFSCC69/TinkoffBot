'''All classes and models module

default classes structure is
response -> Optional[container] -> Optional[list] ->
object -> Optional[subobject]
'''

from typing import Optional, Any
from decimal import Decimal
from pydantic import BaseModel, Field


class TinkoffBaseResponse(BaseModel):
    '''Base parent response model'''
    tracking_id: str = Field(alias='trackingId')
    status: str
    payload: Any

class TinkoffErrorMessage(BaseModel):
    '''Error content'''
    message: str
    code: str

class TinkoffErrorObject(TinkoffBaseResponse):
    '''Object for easy exception parsing'''
    payload: TinkoffErrorMessage

class Empty(TinkoffBaseResponse):
    '''
    Response for
    /orders/cancel
    '''
    payload: dict[None, None]

class MoneyAmount(BaseModel):
    '''
    SubObject for
    /portfolio
    /orders/limit-order
    /orders/market-order
    /operations
    '''
    currency: str
    value: Decimal

class Order(BaseModel):
    '''
    Object for
    /orders
    '''
    order_id: str = Field(alias='orderId')
    figi: str
    operation: str
    status: str
    requested_lots: int = Field(alias='requestedLots')
    executed_lots: int = Field(alias='executedLots')
    type_of_order: str = Field(alias='type')
    price: Decimal

class OrdersResponse(TinkoffBaseResponse):
    '''
    Response for
    /orders
    OrdersResponse(as response) ->
    list[Order] ->
    Order(as object)
    '''
    payload: list[Order]

class LimitOrderRequest(BaseModel):
    '''
    Request for
    /orders/limit-order
    '''
    lots: int
    operation: str
    price: Decimal

class PlacedLimitOrder(BaseModel):
    '''
    Object for
    /orders/limit-order
    '''
    order_id: str = Field(alias='orderId')
    operation: str
    status: str
    reject_reason: Optional[str] = Field(alias='rejectReason')
    message: Optional[str]
    requested_lots: Optional[int] = Field(alias='requestedLots')
    executed_lots: Optional[int] = Field(alias='executedLots')
    commission: Optional[MoneyAmount]

class LimitOrderResponse(TinkoffBaseResponse):
    '''
    Response for
    /orders/limit-order

    LimitOrderResponse(response) ->
    list[PlacedLimitOrder]
    PlacedLimitOrder(object)
    '''
    payload: PlacedLimitOrder

class MarketOrderRequest(BaseModel):
    '''
    Request for
    /orders/market-order
    '''
    lots: int
    operation: str

class PlacedMarketOrder(BaseModel):
    '''
    Object for
    /orders/market-order
    '''
    order_id: str = Field(alias='orderId')
    operation: str
    status: str
    reject_reason: Optional[str] = Field(alias='rejectReason')
    message: Optional[str]
    requested_lots: Optional[int] = Field(alias='requestedLots')
    executed_lots: Optional[int] = Field(alias='executedLots')
    commission: Optional[MoneyAmount]

class MarketOrderResponse(TinkoffBaseResponse):
    '''
    Response for
    /orders/market-order

    MarketOrderResponse(response) ->
    list[PlacedMarketOrder] ->
    PlacedMarketOrder(object)
    '''
    payload: PlacedMarketOrder

class Position(BaseModel):
    '''
    Object for
    /portfolio
    '''
    figi: str
    ticker: Optional[str]
    isin: Optional[str]
    instrument_type: str = Field(alias='instrumentType')
    balance: Decimal
    blocked: Optional[Decimal]
    expected_yield: Optional[MoneyAmount] = Field(alias='expectedYield')
    lots: int
    average_position_price: Optional[MoneyAmount] = Field(alias='averagePositionPrice')
    average_position_price_no_nkd: Optional[MoneyAmount] = Field(alias='averagePositionPriceNoNkd')
    name: str

class Portfolio(BaseModel):
    '''
    List for
    /portfolio
    '''
    positions: list[Position]

class PortfolioResponse(TinkoffBaseResponse):
    '''
    Response for
    /portfolio

    PortfolioResponse(response) ->
    Portfolio(list) ->
    Position(object)
    '''
    payload: Portfolio

class CurrencyPosition(BaseModel):
    '''
    Object for
    /portfolio/currecies
    '''
    currency: str
    balance: Decimal
    blocked: Optional[Decimal]

class Currencies(BaseModel):
    '''
    List for
    /portfolio/currecies
    '''
    currencies: list[CurrencyPosition]

class PortfolioCurrenciesResponse(TinkoffBaseResponse):
    '''
    Response for
    /portfolio/currecies

    PortfolioCurrenciesResponse(response) ->
    Currencies(list) ->
    CurrencyPosition(object)
    '''
    payload: Currencies

class OrderResponse(BaseModel):
    '''
    Object for
    /market​/orderbook
    '''
    price: Decimal
    quantity: int

class OrderBook(BaseModel):
    '''
    Container for
    /market​/orderbook
    '''
    figi: str
    depth: int
    bids: list[OrderResponse]
    asks: list[OrderResponse]
    trade_status: Optional[str] = Field(alias='TradeStatus')
    min_price_increment: Decimal = Field(alias='minPriceIncrement')
    face_value: Optional[Decimal] = Field(alias='faceValue')
    last_price: Optional[Decimal] = Field(alias='lastPrice')
    close_price: Optional[Decimal] = Field(alias='closePrice')
    limit_up: Optional[Decimal] = Field(alias='limitUp')
    limit_down: Optional[Decimal] = Field(alias='limitDown')

class OrderbookResponse(TinkoffBaseResponse):
    '''
    Response for
    /market​/orderbook

    OrderbookResponse(response) ->
    OrderBook(container) -> 2 lists 'bids' and 'asks' of
    OrderResponse(object)
    '''
    payload: OrderBook

class SearchMarketInstrument(BaseModel):
    '''
    Object for
    /market/search/by-figi
    '''
    figi: str
    ticker: str
    isin: Optional[str]
    min_price_increment: Optional[Decimal] = Field(alias='minPriceIncrenent')
    lot: int
    currency: Optional[str]
    name: str
    type_of_intrument: str = Field(alias='type')
    message: Optional[str]

class SearchMarketInstumentResponse(TinkoffBaseResponse):
    '''
    Response for
    /market/search/by-figi

    SearchMarketInstumentResponse(response) ->
    list[SearchMarketInstrument]
    SearchMarketInstrument(object)
    '''
    payload: SearchMarketInstrument

class MarketInstrument(BaseModel):
    '''
    Object for
    /market/search/by-ticker
    '''
    figi: str
    ticker: str
    isin: Optional[str]
    min_price_increment: Optional[Decimal] = Field(alias='minPriceIncrenent')
    lot: int
    min_quantity: Optional[int] = Field(alias='minQuantity')
    currency: Optional[str]
    name: str
    type_of_intrument: str = Field(alias='type')

class MarketInstrumentList(BaseModel):
    '''
    List for
    /market/search/by-ticker
    '''
    total: int
    instruments: list[MarketInstrument]

class MarketInstrumentListResponse(TinkoffBaseResponse):
    '''
    Response for
    /market/search/by-ticker

    MarketInstrumentListResponse(response) ->
    MarketInstrumentList(list) ->
    MarketInstrument(object)
    '''
    payload: MarketInstrumentList

class OperationTrade(BaseModel):
    '''
    SubObject for
    /operations
    '''
    trade_id: str = Field(alias='tradeId')
    date: str
    price: Decimal
    quantity: int

class Operation(BaseModel):
    '''
    Object for
    /operations
    '''
    operation_id: str = Field(alias='id')
    status: str
    trades: Optional[list[OperationTrade]]
    commission: Optional[MoneyAmount]
    currency: str
    payment: Decimal
    price: Optional[Decimal]
    quantity: Optional[int]
    quantity_executed: Optional[int] = Field(alias='quantityExecuted')
    figi: Optional[str]
    instrument_type: Optional[str] = Field(alias='instrumentType')
    isMarginCall: bool
    date: str
    operation_type: Optional[str] = Field(alias='operationType')

class Operations(BaseModel):
    '''
    List for
    /operations
    '''
    operations: list[Operation]

class OperationsResponse(TinkoffBaseResponse):
    '''
    Response for
    /operations

    OperationsResponse(response) ->
    Operations(list) ->
    Operation(object)
    '''
    payload: Operations

class UserAccount(BaseModel):
    '''
    Object for
    /user/accounts
    '''
    broker_account_id: str = Field(alias='brokerAccountId')
    broker_account_type: str = Field(alias='brokerAccountType')

class UserAccounts(BaseModel):
    '''
    List for
    /user/accounts
    '''
    accounts: list[UserAccount]

class UserAccountsResponse(TinkoffBaseResponse):
    '''
    Response for
    /user/accounts

    UserAccountsResponse(response) ->
    UserAccounts(list) ->
    UserAccount(object)
    '''
    payload: UserAccounts
