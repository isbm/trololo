"""
Trololo exceptions.
"""


class UnauthorisedError(Exception):
    """
    User is unauthorised
    """


class UnknownResourceError(Exception):
    """
    Resource not found.
    """


class RequestError(Exception):
    """
    Trello request error
    """


class CLIError(Exception):
    """
    CLI error
    """
