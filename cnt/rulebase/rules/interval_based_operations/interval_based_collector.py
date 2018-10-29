"""
Collect the unicode codepoint specified by intervals.
"""
from typing import Any

from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import IntervalBasedOperation


class _IntervalBasedCollectorOutputGenerator(workflow.BasicOutputGenerator):

    def _result(self) -> workflow.CommonOutputLazyType:
        while True:
            try:
                index, label = next(self.label_processor_result)
            except StopIteration:
                return
            if not label:
                continue

            start = index
            end = -1
            try:
                while True:
                    index, label = next(self.label_processor_result)
                    if not label:
                        end = index
                        break
            except StopIteration:
                end = len(self.input_sequence)

            yield self.input_sequence[start:end], (start, end)

    def result(self) -> Any:
        raise NotImplementedError()


class IntervalBasedCollectorOutputGeneratorLazy(_IntervalBasedCollectorOutputGenerator):

    def result(self) -> workflow.CommonOutputLazyType:
        return self._result()


class IntervalBasedCollectorOutputGenerator(_IntervalBasedCollectorOutputGenerator):

    def result(self) -> workflow.CommonOutputType:
        return list(self._result())


class IntervalBasedCollector(IntervalBasedOperation):

    OUTPUT_GENERATOR_LAZY = IntervalBasedCollectorOutputGeneratorLazy
    OUTPUT_GENERATOR = IntervalBasedCollectorOutputGenerator
