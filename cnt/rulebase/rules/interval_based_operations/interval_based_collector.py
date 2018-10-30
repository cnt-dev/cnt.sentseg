"""
Collect the unicode codepoint specified by intervals.
"""
from typing import Any

from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import BasicIntervalBasedOperation


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


class IntervalBasedCollectorLazy(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedCollectorOutputGeneratorLazy

    def result(self, text: str) -> workflow.CommonOutputLazyType:
        return self.interval_based_workflow.result(text)


class IntervalBasedCollector(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedCollectorOutputGenerator

    def result(self, text: str) -> workflow.CommonOutputType:
        return self.interval_based_workflow.result(text)
