from datetime import timedelta


def parse_duration(duration):
    hours = None
    minutes = None

    if duration.isdigit():
        hours = int(duration)
    elif ':' in duration:
        duration_split = duration.split(':')
        hours = int(duration_split[0])
        minutes = int(duration_split[1])
    elif '.' in duration:
        duration_split = duration.split('.')
        hours = int(duration_split[0])
        minutes = int(60 * float('.' + duration_split[1]))

    if hours == None:
        hours = 0
    if minutes == None:
        minutes = 0

    if hours or minutes:
        return timedelta(hours=hours, minutes=minutes)
    else:
        raise ValueError('Could not parse duration.')
