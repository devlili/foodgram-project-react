from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Переопределение названия поля,
    отвечающего за количество результатов в выдаче."""

    page_size = 6
    page_size_query_param = "limit"
