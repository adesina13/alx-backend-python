# chats/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    """
    Pagination class for messages.
    - Default page size: 20
    - Supports `page_size` query param to override
    - Max page size: 100
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Customize the paginated response to include:
        - total count (page.paginator.count)
        - next and previous page links
        - results (messages)
        """
        return Response({
            "count": self.page.paginator.count,  # total number of messages
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })
