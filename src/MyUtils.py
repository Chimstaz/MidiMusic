"""Useful pieces of codes."""


def coalesce(*arg):
    """Return first not None element."""
    for el in arg:
        if el is not None:
            return el
    return None
