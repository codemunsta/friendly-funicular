from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    page_size = 20
    page_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = {
            'count': self.page.paginator.count,
            'next': self.get_next_page_number(),
            'next_link': self.get_next_link(),
            'previous': self.get_previous_page_number(),
            'previous_link': self.get_previous_link(),
            'results': data
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
