import itertools


def get_offsets(n, top=False, bottom=False, left=False, right=False):
    if not top and not bottom and not left and not right:
        offsets = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if top:
        if right:
            offsets = [(0, -1), (-1, -1), (-1, 0)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        if left:
            offsets = [(1, 0), (1, -1), (0, -1)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        offsets = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if bottom:
        if right:
            offsets = [(-1, 0), (-1, 1), (0, 1)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        if left:
            offsets = [(1, 1), (1, 0), (0, 1)]
            return [offset_set for offset_set in itertools.combinations(offsets, n)]
        offsets = [(1, 1), (1, 0), (-1, 0), (-1, 1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if right:
        offsets = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    if left:
        offsets = [(1, 1), (1, 0), (1, -1), (0, -1), (0, 1)]
        return [offset_set for offset_set in itertools.combinations(offsets, n)]
    
