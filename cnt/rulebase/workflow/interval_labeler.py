from typing import List, Optional
from typing import re as BuiltInReType
import re

from cnt.rulebase.workflow.basic_workflow import BasicSequentialLabeler
from cnt.rulebase.workflow.type_annotations import IntervalType, IntervalGeneratorType


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

    ITV_RE_PATTERN = None

    @classmethod
    def initialize_by_regular_expression(cls, pattern: str) -> None:
        cls.ITV_RE_PATTERN = re.compile(pattern, re.UNICODE)

    @classmethod
    def initialize_by_intervals(cls, intervals: List[IntervalType]) -> None:
        """
        Convert intervals to regular expression pattern.

        :param intervals: Unicode codepoint intervals.
        """

        inner = [f'{chr(lb)}-{chr(ub)}' for lb, ub in intervals]
        joined_inner = ''.join(inner)
        pattern = f'[{joined_inner}]+'

        cls.initialize_by_regular_expression(pattern)

    def __init__(self, input_sequence: str):
        super().__init__(input_sequence)

        self.intervals = self.intervals_generator()
        self.cur_interval = _next_interval(self.intervals)

    def intervals_generator(self) -> IntervalGeneratorType:
        if self.ITV_RE_PATTERN is None:
            raise RuntimeError('ITV_RE_PATTERN should be initialized.')
        return (match.span() for match in self.ITV_RE_PATTERN.finditer(self.input_sequence))

    def label(self, index: int) -> bool:
        if self.cur_interval is None or index < self.cur_interval[0]:
            return False

        if index < self.cur_interval[1]:
            return True

        self.cur_interval = _next_interval(self.intervals)
        return False
