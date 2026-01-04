from rest_framework.pagination import PageNumberPagination

class LMSResultsSetPagination(PageNumberPagination):
    page_size = 15               # default items per page
    page_size_query_param = 'page_size'  # allow client to set page size
    max_page_size =50     # maximum items per page


