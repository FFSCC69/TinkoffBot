TinkoffBot
auto-trading using tinkoff api, email and trading view


TradingView strategy alert message:

MESSAGE_START{"order_action": "{{strategy.order.action}}",
 "quantity": {{strategy.order.contracts}}, "price": {{strategy.order.price}},
  "ticker": "{{ticker}}", "position": {{strategy.position_size}}, "time": "{{timenow}}"}MESSAGE_END
