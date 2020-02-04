import operator
from collections import defaultdict
from functools import reduce


def infinite_defaultdict():
    return defaultdict(infinite_defaultdict)


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    try:
        return reduce(operator.getitem, items, root)
    except KeyError:
        return None


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


def ensure_path_exists(root, items):
    cur = root
    for i in items:
        if i not in cur:
            cur[i] = {}
        cur = cur[i]
