import itertools


def get_offsets(n):
    offsets = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
    return [offset_set for offset_set in itertools.combinations(offsets, n)]
