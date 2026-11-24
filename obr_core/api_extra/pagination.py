from rest_framework import pagination


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    # cap client-provided `limit` (default page size is set via `PAGE_SIZE`)
    max_limit = 200
