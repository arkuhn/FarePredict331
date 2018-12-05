from datetime import datetime
import holidays

def isRushour(dt):
    """
    4pm - 6pm -> Military -> 16 - 19
    5am - 9am -> Military -> 5 - 9
    """
    if ((dt.hour >= 5 and dt.hour <= 9) or (dt.hour >= 16 and dt.hour <= 19)):
        return 1
    return 0

def isWeekend(dt):
    if (dt.weekday() < 5):
        return 0
    return 1

def isHoliday(dt):
    #[(month, day), (month, day)...]
    us_holidays = holidays.UnitedStates()
    if datetime(dt.year, dt.month, dt.day) in us_holidays:
        return 1
    return 0

def nHour(dt):
    MAX_HOUR=24
    return round(dt.hour / MAX_HOUR, 4)

def nDay(dt):
    MAX_DAY=6
    return round(dt.weekday() / MAX_DAY, 3)

def nMonth(dt):
    MAX_MONTH=12
    return round(dt.month / MAX_MONTH, 3)

def nYear(dt):
    MAX_YEAR=2015
    return round(dt.year / MAX_YEAR, 3)

def processDates(datetimeString):
    dtObject = datetime.strptime(datetimeString, '%Y-%m-%d %H:%M:%S %Z')
    return (isRushour(dtObject), isWeekend(dtObject), isHoliday(dtObject), 
            nHour(dtObject), nDay(dtObject), nMonth(dtObject), nYear(dtObject))