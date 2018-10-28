from typing import Generator, List, Tuple, Optional
from typing import re as BuiltInReType
import re

from cnt.rulebase.workflow.basic_workflow import BasicSequentialLabeler

IntervalType = Tuple[int, int]
IntervalGeneratorType = Generator[IntervalType, None, None]


def _next_interval(intervals: IntervalGeneratorType) -> Optional[IntervalType]:
    try:
        return next(intervals)
    except StopIteration:
        return None


class IntervalLabeler(BasicSequentialLabeler):
    """
    Helper to label intervals.

    :param input_sequence: The input sequence.
    """

    def __init__(self, input_sequence: str):
        super().__init__(input_sequence)

        self.intervals = self.initialize_intervals()
        self.cur_interval = _next_interval(self.intervals)

    def initialize_intervals(self) -> IntervalGeneratorType:
        raise NotImplementedError()

    def label(self, index: int) -> bool:
        if self.cur_interval is None or index < self.cur_interval[0]:
            return False

        if index < self.cur_interval[1]:
            return True

        self.cur_interval = _next_interval(self.intervals)
        return False


def re_pattern_from_intervals(intervals: List[IntervalType]) -> BuiltInReType:
    """
    Convert intervals to regular expression pattern.

    :param intervals: Unicode codepoint intervals.
    """

    inner = [f'{chr(lb)}-{chr(ub)}' for lb, ub in intervals]
    joined_inner = ''.join(inner)
    pattern = f'[{joined_inner}]+'

    return re.compile(pattern, re.UNICODE)
