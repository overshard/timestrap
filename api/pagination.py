from collections import OrderedDict

from django.db.models import Sum

from rest_framework.pagination import LimitOffsetPagination, _get_count
from rest_framework.response import Response

from core.utils import duration_string_from_delta


class LimitOffsetPaginationWithTotals(LimitOffsetPagination):
    total_duration = None
    subtotal_duration = None

    def paginate_queryset(self, queryset, request, view=None):
        self.total_duration = (queryset
                               .aggregate(Sum('duration'))['duration__sum'])

        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.count = _get_count(queryset)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []

        queryset = queryset[self.offset:self.offset + self.limit]
        self.subtotal_duration = (queryset
                                  .aggregate(Sum('duration'))['duration__sum'])

        return list(queryset)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('total_duration', duration_string_from_delta(self.total_duration)),
            ('subtotal_duration', duration_string_from_delta(self.subtotal_duration)),
            ('results', data)
	]))
