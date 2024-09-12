from rest_framework import pagination


class ServicePaginator(pagination.PageNumberPagination):
    page_size = 4


class commonPaginator(pagination.PageNumberPagination):
    page_size = 4
