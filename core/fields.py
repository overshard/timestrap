from datetime import timedelta

from six import text_type

from rest_framework.fields import DurationField

from .utils import parse_duration, duration_decimal


class DurationField(DurationField):
    def to_internal_value(self, value):
        if isinstance(value, timedelta):
            return value
        parsed = parse_duration(text_type(value))
        if parsed is not None:
            return parsed
        else:
            return None
        self.fail("invalid", format="[[HH]:MM] or [[HH][.MM]]")

    def to_representation(self, value):
        return duration_decimal(value)
