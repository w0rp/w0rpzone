import sys

from functools import wraps


def print_return_value(func):
    """
    This decorator prints the repr of the return value of any given function to
    stderr and passes it along.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)

        print(repr(result))

        return result

    return inner
