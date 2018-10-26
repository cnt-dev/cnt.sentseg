"""
Basic Workflow.
"""
from typing import Iterable, Type, Generator, Dict, Tuple


class BasicSequentialLabeler:
    """
    Define the interface of SequentialLabeler.

    :param input_sequence: The input sequence.
    """

    def __init__(self, input_sequence: str):
        self.input_sequence = input_sequence

    def label(self, index: int) -> bool:
        """
        Return boolean label for ``self.input_sequence[index]``.
        Derived class must override this method.

        :param index: The index of ``self.input_sequence``.
        """
        raise NotImplementedError('label')


IndexLabelsType = Tuple[int, Dict[Type[BasicSequentialLabeler], bool]]
IndexLabelsGeneratorType = Generator[IndexLabelsType, None, None]


class BasicLabelProcessor:
    """
    Define the interface of LabelProcessor.

    :param index_labels_generator: ``(index, labels)`` generated from
        one or more :class:`BasicSequentialLabeler`.
    """

    def __init__(self, index_labels_generator: IndexLabelsGeneratorType):
        self.index_labels_generator = index_labels_generator


class BasicWorkflow:
    """
    Define the basic workflow.
    Use composite pattern to organize the steps of rule-based processing.

    :param sequential_labeler_classes: For char-level sequential labeling.
    :param label_processor_class: Label post-processing.
        Commonly this step will generate new labels based on
        the result of ``sequential_labeler_classes``.
    """

    def __init__(
            self,
            sequential_labeler_classes: Iterable[Type[BasicSequentialLabeler]],
            label_processor_class: Type[BasicLabelProcessor],
    ):
        pass
