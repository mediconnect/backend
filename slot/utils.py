from datetime import datetime


def date_to_weeknum(date):
    year, weeknum, _ = date.isocalendar()
    return year, weeknum


def weeknum_to_date(year, weeknum):
    return datetime.strptime("{yr},{wk},1".format(yr=year, wk=weeknum-1), "%Y,%W,%w").date()