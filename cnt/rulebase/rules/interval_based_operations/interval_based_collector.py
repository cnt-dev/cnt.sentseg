"""
Collect the unicode codepoint specified by intervals.
"""
from typing import Type, Any, Generator, List, Tuple

from cnt.rulebase import workflow


class IntervalBasedRuleLabelProcessor(workflow.BasicLabelProcessor):

    def result(self) -> Generator[Tuple[int, bool], None, None]:
        while True:
            try:
                index, labels = next(self.index_labels_generator)
            except StopIteration:
                return

            # workflow.labelType -> bool
            yielded = False
            for label in labels.values():
                if label:
                    yield index, True
                    yielded = True
                    break
            if not yielded:
                yield index, False


class _IntervalBasedRuleOutputGenerator(workflow.BasicOutputGenerator):

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


class IntervalBasedRuleOutputGeneratorLazy(_IntervalBasedRuleOutputGenerator):

    def result(self) -> workflow.CommonOutputLazyType:
        return self._result()


class IntervalBasedRuleOutputGenerator(_IntervalBasedRuleOutputGenerator):

    def result(self) -> workflow.CommonOutputType:
        return list(self._result())


def _generate_interval_labeler_class() -> Type[workflow.IntervalLabeler]:

    class DerivedIntervalLabeler(workflow.IntervalLabeler):
        pass

    return DerivedIntervalLabeler


class IntervalBasedRule:

    OUTPUT_GENERATOR_LAZY = workflow.BasicOutputGenerator
    OUTPUT_GENERATOR = workflow.BasicOutputGenerator

    def __init__(self, intervals: List[workflow.IntervalType]):
        # Labeler.
        self.sequential_labeler_class = _generate_interval_labeler_class()
        self.sequential_labeler_class.initialize_by_intervals(intervals)

        # Workflow.
        self.interval_based_workflow_lazy = self._generate_workflow(lazy=True)
        self.interval_based_workflow = self._generate_workflow(lazy=False)

    def _generate_workflow(self, lazy: bool) -> workflow.BasicWorkflow:
        return workflow.BasicWorkflow(
                sequential_labeler_classes=[self.sequential_labeler_class],
                label_processor_class=IntervalBasedRuleLabelProcessor,
                output_generator_class=(self.OUTPUT_GENERATOR_LAZY
                                        if lazy else self.OUTPUT_GENERATOR),
        )

    def result_lazy(self, text: str) -> workflow.CommonOutputLazyType:
        return self.interval_based_workflow_lazy.result(text)

    def result(self, text) -> workflow.CommonOutputType:
        return self.interval_based_workflow.result(text)


class IntervalBasedCollector(IntervalBasedRule):

    OUTPUT_GENERATOR_LAZY = IntervalBasedRuleOutputGeneratorLazy
    OUTPUT_GENERATOR = IntervalBasedRuleOutputGenerator
