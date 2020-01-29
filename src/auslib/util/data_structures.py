from collections import defaultdict


def infinite_defaultdict():
    return defaultdict(infinite_defaultdict)
