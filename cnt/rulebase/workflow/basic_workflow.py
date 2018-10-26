"""
Basic Workflow.
"""
from typing import Iterable, Type, Generator, Any, Dict, Tuple


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
        raise NotImplementedError()


IndexLabelsType = Tuple[int, Dict[Type[BasicSequentialLabeler], bool]]
IndexLabelsGeneratorType = Generator[IndexLabelsType, None, None]


class BasicLabelProcessor:
    """
    Define the interface of LabelProcessor.

    :param input_sequence: The input sequence.
    :param index_labels_generator: ``(index, labels)`` generated from
        one or more :class:`BasicSequentialLabeler`.
    """

    def __init__(self, input_sequence: str, index_labels_generator: IndexLabelsGeneratorType):
        self.input_sequence = input_sequence
        self.index_labels_generator = index_labels_generator

    def result(self) -> Any:
        """
        Label processor could generate any return type.
        Derived class must override this method.
        """
        raise NotImplementedError()


class BasicOutputGenerator:
    """
    Define the interface of OutputGenerator.

    :param input_sequence: The input sequence.
    :param label_processor_result: The result of :class:`BasicLabelProcessor`.
    """

    def __init__(self, input_sequence: str, label_processor_result: Any):
        self.input_sequence = input_sequence
        self.label_processor_result = label_processor_result

    def result(self) -> Any:
        """
        Output generator could generate any return type.
        Derived class must override this method.
        """
        raise NotImplementedError()


class BasicWorkflow:
    """
    Define the basic workflow.
    Use composite pattern to organize the steps of rule-based processing.

    :param sequential_labeler_classes: For char-level sequential labeling.
    :param label_processor_class: Label post-processing.
        Commonly this step will generate new labels based on
        the result of ``sequential_labeler_classes``.
    :param output_generator_class: Generate output based on input sequence & labels.
    """

    def __init__(self, sequential_labeler_classes: Iterable[Type[BasicSequentialLabeler]],
                 label_processor_class: Type[BasicLabelProcessor],
                 output_generator_class: Type[BasicOutputGenerator]):
        self.sequential_labeler_classes = sequential_labeler_classes
        self.label_processor_class = label_processor_class
        self.output_generator_class = output_generator_class

    def result(self, input_sequence: str) -> Any:
        """
        Execute the workflow.

        :param input_sequence: The input sequence.
        """
        pass
