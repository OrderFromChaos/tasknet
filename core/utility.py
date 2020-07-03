from datetime import datetime, timedelta

def naturaldate(truedate):
    # Possible outputs:
    # Jan 21, 2052 (if 11:59pm and date is not current year)
    # Jan 21 (if 11:59pm and date is this year)
    # Thursday (if the date is this week and 11:59pm)
    # next Thursday (if date is next week and 11:59pm)
    # X 10:00am (if the due date is not 11:59 on the previous options)
    # TODO: Allow additional fuzziness (like "a month from now" or something)
    #       in config
    output = []
    now = datetime.now()
    # Assuming day of the week starts on Sunday
    nowmorn = datetime(now.year, now.month, now.day)
    floorweek = nowmorn - timedelta(days=(nowmorn.weekday()+1) % 7)
    ceilweek = floorweek + timedelta(days=6, hours=23, minutes=59)
    lastweek = floorweek - timedelta(days=7)
    nextweek = ceilweek + timedelta(days=7)

    if lastweek <= truedate < floorweek:
        output.append('last')
        output.append(truedate.strftime(r'%A'))
    elif floorweek <= truedate <= ceilweek:
        output.append(truedate.strftime(r'%A'))
    elif ceilweek < truedate <= nextweek:
        output.append('next')
        output.append(truedate.strftime(r'%A'))
    else:
        output.append(truedate.strftime(r'%b %d'))
        if now.year != truedate.year:
            output.append(truedate.strftime(r'%Y'))

    if truedate.strftime(r'%I:%M%p') != '11:59PM':
        output.append(truedate.strftime(r'%I:%M%p'))

    return ' '.join(output)