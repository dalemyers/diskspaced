"""Defer blocks of code to be executed later."""

from contextlib import contextmanager


@contextmanager
def defer():
    """Defer blocks of code to be executed later."""

    deferred_calls = []

    try:
        yield deferred_calls.append
    finally:
        while deferred_calls:
            func = deferred_calls.pop()
            func()
