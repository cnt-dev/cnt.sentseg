"""
Collect the unicode codepoint specified by intervals.
"""
from typing import Type, Generator, List, Tuple

from cnt.rulebase import workflow


class IntervalBasedOperationLabelProcessor(workflow.BasicLabelProcessor):

    def result(self) -> Generator[Tuple[int, bool], None, None]:
        while True:
            try:
                index, labels = next(self.index_labels_generator)
            except StopIteration:
                return

            # workflow.labelType -> bool
            marked = False
            for label in labels.values():
                if label:
                    marked = True
                    break
            yield index, marked


def _generate_interval_labeler_class() -> Type[workflow.IntervalLabeler]:

    class DerivedIntervalLabeler(workflow.IntervalLabeler):
        pass

    return DerivedIntervalLabeler


class IntervalBasedOperation:

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
                label_processor_class=IntervalBasedOperationLabelProcessor,
                output_generator_class=(self.OUTPUT_GENERATOR_LAZY
                                        if lazy else self.OUTPUT_GENERATOR),
        )

    def result_lazy(self, text: str) -> workflow.CommonOutputLazyType:
        return self.interval_based_workflow_lazy.result(text)

    def result(self, text) -> workflow.CommonOutputType:
        return self.interval_based_workflow.result(text)
