"""Utils functions (DEPRECATED)"""
import itertools
import bisect
from typing import Iterable, List, Tuple, Callable


def generate_range_checker(sorted_intervals: List[Tuple[int, int]]) -> Callable[[str], bool]:
    """To check if a char is in ranges."""
    ranges_start = [t[0] for t in sorted_intervals]

    def _char_in_range(char: str) -> bool:
        code_point = ord(char)

        # 1. find a range such that (start, end), start <= code_point.
        idx = bisect.bisect_left(ranges_start, code_point)
        if idx == len(ranges_start) or \
                (idx != 0 and code_point != ranges_start[idx]):
            idx -= 1

        # 2. check if start <= code_point <= end.
        # (to deal with the coner case when idx == 0).
        return sorted_intervals[idx][0] <= code_point <= sorted_intervals[idx][1]

    return _char_in_range
