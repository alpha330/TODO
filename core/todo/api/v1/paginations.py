from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):
    """_summary_
    in pagination.py at api apss can deploy paginator class
    to paginate pages of data comes from model apps
    attributes:
    here can change page_size th size of datafields in page
    """

    page_size = 5

    def get_paginated_response(self, data):
        """_summary_
        get pagination deta and can rewrite or add values in pagination form
        """
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total_objects": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
