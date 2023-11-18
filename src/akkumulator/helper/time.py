from datetime import datetime


def today():
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    return datetime(year, month, day)


def influx_time_to_datetime(time: str, ms: bool = True):
    try:
        dt = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        dt = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    if ms:
        dt = dt.replace(microsecond=0)
    return dt


def dt_to_influx(time: datetime, ms: bool = True):
    return time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')