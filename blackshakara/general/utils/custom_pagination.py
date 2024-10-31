import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    page_size = 15
    page_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = {
            'count': self.page.paginator.count,
            'next': self.get_next_page_number(),
            'next_link': self.get_next_link(),
            'previous': self.get_previous_page_number(),
            'previous_link': self.get_previous_link(),
            'total_pages': self.get_total_page(),
            'current_page': self.get_current_page(),
            'data': data
        }
        return Response(response)

    def get_next_page_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_total_page(self):
        total = int(self.page.paginator.count) / int(self.page_size)
        return math.ceil(total)

    def get_current_page(self):
        if self.get_previous_page_number() is None:
            return 1
        else:
            return int(self.get_previous_page_number()) + 1
