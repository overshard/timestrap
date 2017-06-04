from __future__ import division

from django.utils.duration import _get_duration_components

from datetime import timedelta

from decimal import Decimal


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
        # TODO: Fix error here when not appending a 0, ex .5 instead of 0.5
        hours = int(duration_split[0])
        minutes = int(60 * float('.' + duration_split[1]))

    if minutes is None:
        minutes = 0

    if hours or minutes:
        return timedelta(hours=hours, minutes=minutes)
    else:
        return None


def duration_string(duration):
    if duration is not None:
        days, hours, minutes, seconds, microseconds = _get_duration_components(duration)  # noqa: E501
        hours += days * 24

        string = '{}:{:02d}'.format(hours, minutes)
    else:
        string = '0:00'
    return string


def duration_decimal(duration):
    if duration is not None:
        days, hours, minutes, seconds, microseconds = _get_duration_components(duration)  # noqa: E501
        hours += days * 24

        decimal = Decimal(hours) + Decimal(minutes/60)
    else:
        decimal = Decimal(0)
    return decimal
