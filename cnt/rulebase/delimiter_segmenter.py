"""Delimiter segmenter."""
from typing import List, Tuple

from cnt.rulebase import const, segmenter_common

SEGMENT_RANGES = const.sorted_chain(
        const.ITV_CHINESE_CHARS,
        const.ITV_ENGLISH_CHARS,
        const.ITV_DIGITS,
)


def _dlmseg_start_cond_fn(start: int, marks_group: segmenter_common.MarksGroupType) -> bool:
    segments: List[bool] = marks_group[0]
    return segments[start]


def _dlmseg_end_cond_fn(end: int, marks_group: segmenter_common.MarksGroupType) -> Tuple[bool, int]:
    segments: List[bool] = marks_group[0]
    if segments[end]:
        return False, end + 1
    return True, end


dlmseg = segmenter_common.generate_segmenter(  # pylint: disable=invalid-name
        [
                segmenter_common.generate_ranges_marker(SEGMENT_RANGES),
        ],
        _dlmseg_start_cond_fn,
        _dlmseg_end_cond_fn,
)
