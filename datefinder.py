"""
Finds new chart dates between specified start and end dates -
warning, the official chart day switched from Sunday to Friday in 2018
"""

import datetime
import math


def datefinder(newestdate, oldestdate):

    dates = []
    date_delta = datetime.datetime.strptime(newestdate, '%Y/%m/%d') - datetime.datetime.strptime(oldestdate, '%Y/%m/%d')
    weeks = int(math.floor(date_delta.days/7))
    for x in range(weeks+1):
        date = datetime.datetime.strptime(newestdate, '%Y/%m/%d') - datetime.timedelta(days=7*x)
        date = date.strftime('%Y%m%d')
        dates.append(date)

    return dates

