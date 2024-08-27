"""Set the recursion limit temporarily."""

import sys


class TemporaryRecursionLimit:
    """Set the recursion limit temporarily."""

    limit: int
    previous_limit: int | None

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.previous_limit = None

    def __enter__(self):
        self.previous_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.previous_limit)
