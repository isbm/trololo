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


class CLIError(Exception):
    """
    CLI error
    """
