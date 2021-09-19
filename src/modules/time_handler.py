'''Converting timezones and time strings'''
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import *
from pytz import timezone, utc
from ..settings import TIME_ZONE_LOCAL, TIME_ZONE_UTC


local_timezone = timezone(TIME_ZONE_LOCAL)
utc_timezone = timezone(TIME_ZONE_UTC)
now = datetime.now(local_timezone).replace(microsecond=0)
print(now)

utc_dt = parse('2021-09-17T13:50:00Z')
local_dt = utc_dt.replace(tzinfo=utc).astimezone(local_timezone)
print(local_dt)