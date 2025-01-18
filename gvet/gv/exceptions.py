class GVException(Exception):
    """Base exception class"""

    ...


class ObjectDoesNotExist(GVException):
    """When an object is expected in a query result but does not exist."""

    ...
