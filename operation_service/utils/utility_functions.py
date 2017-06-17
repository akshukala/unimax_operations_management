from datetime import datetime
import pytz

def get_iso_date(date):
    try:
        return datetime.strptime(date, '%d-%B-%Y').strftime('%Y-%m-%d')
    except:
        return

def get_str_date(date):
    try:
        return date.strftime('%d-%B-%Y')
    except:
        return ''

def utc_to_time(naive, timezone="Asia/Kolkata"):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))

def get_str_datetime(date):
    try:
        return date.strftime('%d %b %Y %H:%M')
    except:
        return ''

