"""Constants."""

ACCEPTABLE_OS_ERRORS = set(
    [
        1,  # Operation not permitted
        9,  # Bad file descriptor
        13,  # Permission denied
    ]
)

MAX_RECURSION_LIMIT = 10_000
