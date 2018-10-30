"""
Replace the unicode codepoint specified by intervals with arbitary strings.
"""
from typing import Any

from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import BasicIntervalBasedOperation


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


class IntervalBasedReplacerLazy(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedReplacerOutputGeneratorLazy

    def result(self, text: str) -> workflow.CommonOutputLazyType:
        return self.interval_based_workflow.result(text)


class IntervalBasedReplacer(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedReplacerOutputGenerator

    def result(self, text: str) -> workflow.CommonOutputType:
        return self.interval_based_workflow.result(text)
