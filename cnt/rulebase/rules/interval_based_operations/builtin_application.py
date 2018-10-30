"""
TODO
"""
from typing import Iterable
from cnt.rulebase import const, workflow
from cnt.rulebase.rules.interval_based_operations import (
        interval_based_collector,
        interval_based_replacer,
)


# Built-in collectors.
class BuiltInCollector:

    @classmethod
    def generate_collector(cls, *intervals: Iterable[workflow.IntervalListType]) -> None:
        intervals = const.sorted_chain(*intervals)
        replacer = interval_based_collector.IntervalBasedCollector(intervals)
        replacer_lazy = interval_based_collector.IntervalBasedCollectorLazy(intervals)

        return replacer, replacer_lazy

    @classmethod
    def setup_collector(cls, name: str, *intervals: Iterable[workflow.IntervalListType]) -> None:
        if hasattr(cls, name):
            raise RuntimeError(f'Duplicated name: {name}')

        replacer, replacer_lazy = cls.generate_collector(*intervals)

        setattr(cls, name, replacer)
        setattr(cls, f'{name}_lazy', replacer_lazy)


BuiltInCollector.setup_collector('chinese_chars', const.ITV_CHINESE_CHARS)
BuiltInCollector.setup_collector('english_chars', const.ITV_ENGLISH_CHARS)
BuiltInCollector.setup_collector('digits', const.ITV_DIGITS)
BuiltInCollector.setup_collector('delimiters', const.ITV_DELIMITERS)

BuiltInCollector.setup_collector(
        'chinese_sentence_chars',
        const.ITV_CHINESE_CHARS,
        const.ITV_ENGLISH_CHARS,
        const.ITV_DIGITS,
)
