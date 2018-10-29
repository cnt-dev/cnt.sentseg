"""
Replace the unicode codepoint specified by intervals with arbitary strings.
"""
from typing import Any

from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import IntervalBasedOperation


class _IntervalBasedReplacerOutputGenerator(workflow.BasicOutputGenerator):

    def _result(self) -> workflow.CommonOutputLazyType:
        pass

    def result(self) -> Any:
        raise NotImplementedError()


class IntervalBasedReplacerOutputGeneratorLazy(_IntervalBasedReplacerOutputGenerator):

    def result(self) -> workflow.CommonOutputLazyType:
        return self._result()


class IntervalBasedReplacerOutputGenerator(_IntervalBasedReplacerOutputGenerator):

    def result(self) -> workflow.CommonOutputType:
        return list(self._result())


class IntervalBasedCollector(IntervalBasedOperation):

    OUTPUT_GENERATOR_LAZY = IntervalBasedReplacerOutputGeneratorLazy
    OUTPUT_GENERATOR = IntervalBasedReplacerOutputGenerator
