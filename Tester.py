import pytz
import datetime
from pytz import timezone
todaysdate = datetime.datetime.now(timezone('Europe/Warsaw'))
#.astimezone(pytz.timezone('Europe/Warsaw')))

print(todaysdate)
# timezones = pytz.all_timezones
# for i in timezones:
#     print(i)
