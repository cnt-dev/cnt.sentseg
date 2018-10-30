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


class BasicIntervalBasedOperation:

    OUTPUT_GENERATOR = workflow.BasicOutputGenerator

    def __init__(self, intervals: List[workflow.IntervalType]):
        # Labeler.
        self.sequential_labeler_class = _generate_interval_labeler_class()
        self.sequential_labeler_class.initialize_by_intervals(intervals)

        # OutputGenerator.
        self._output_generator_class = workflow.BasicOutputGenerator
        self.initialize_output_generator_class()

        # Workflow.
        self.interval_based_workflow = self._generate_workflow()

    def initialize_output_generator_class(self) -> None:
        """
        Derived class should override this method by initializing ``self._output_generator_class``.
        """
        raise NotImplementedError()

    def _generate_workflow(self) -> workflow.BasicWorkflow:
        return workflow.BasicWorkflow(
                sequential_labeler_classes=[self.sequential_labeler_class],
                label_processor_class=IntervalBasedOperationLabelProcessor,
                output_generator_class=self._output_generator_class,
        )
