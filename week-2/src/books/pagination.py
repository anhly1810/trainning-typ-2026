import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):
        total_elements = self.page.paginator.count
        size = self.get_page_size(self.request) or self.page_size
        total_pages = math.ceil(total_elements / size) if size else 0

        return Response(
            {
                "data": data,
                "page": self.page.number,
                "size": size,
                "totalPages": total_pages,
                "totalElements": total_elements,
            }
        )
