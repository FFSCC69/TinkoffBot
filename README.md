TinkoffBot
auto-trading using tinkoff api, email and trading view

some usefull files:

bot.py # main file
pip_req.txt # python requirements
startup.py # semiauto startup
src/settings.py # settings

TradingView strategy alert message:

MESSAGE_START{"ticker": "{{ticker}}", "order_action": "{{strategy.order.action}}", "quantity": {{strategy.order.contracts}}, "price": {{strategy.order.price}}, "position": {{strategy.position_size}}, "market_position": "{{strategy.market_position}}", "time": "{{timenow}}"}MESSAGE_END
