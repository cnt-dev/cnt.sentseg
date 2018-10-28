"""
Chinese sentence segmentation.
"""
from typing import Any, Union, Generator, List, Tuple, cast
import re

from cnt.rulebase import workflow
from cnt.rulebase.rules.sentence_segmentation import const as sentseg_const


class SentenceEndingLabeler(workflow.ExactMatchLabeler):
    """
    Mark sentence endings based on
    :py:const:`cnt.rulebase.const.sentence_endings.EM_SENTENCE_ENDINGS`

    Time & space complexity: `O(1)`.
    """
    pass


SentenceEndingLabeler.build_ac_automation_from_strings(sentseg_const.EM_SENTENCE_ENDINGS)


class CommaLabeler(workflow.BasicSequentialLabeler):
    """
    Mark comma.

    Time & space complexity: `O(1)`.
    """

    COMMAS = (chr(0xFF0C), chr(0x201A), ',')

    def label(self, index: int) -> bool:
        return self.input_sequence[index] in self.COMMAS


class WhitespaceLabeler(workflow.IntervalLabeler):
    """
    Mark unicode whitespace.

    Time & space complexity: `O(1)`.
    """

    WHITESPACE_PATTERN = re.compile(r'\s+')

    def initialize_intervals(self) -> workflow.IntervalGeneratorType:
        return (match.span() for match in self.WHITESPACE_PATTERN.finditer(self.input_sequence))


class SentenceValidCharacterLabeler(workflow.IntervalLabeler):
    """
    Mark valid character of chinese sentence.

    Time & space complexity: `O(1)`.
    """

    SENTENCE_VALID_CHARS_PATTERN = workflow.re_pattern_from_intervals(
            sentseg_const.ITV_SENTENCE_VALID_CHARS)

    def initialize_intervals(self) -> workflow.IntervalGeneratorType:
        return (match.span()
                for match in self.SENTENCE_VALID_CHARS_PATTERN.finditer(self.input_sequence))


class SentenceSegementationConfig(workflow.BasicConfig):

    def __init__(self, enable_comma_ending: bool):
        self.enable_comma_ending = enable_comma_ending


class SentenceSegementationLabelProcessor(workflow.BasicLabelProcessor):

    def _labels_indicate_sentence_ending(self, labels: workflow.LabelsType) -> bool:
        return bool(labels[SentenceEndingLabeler] or
                    (self.config.enable_comma_ending and labels[CommaLabeler]))

    def result(self) -> workflow.IntervalGeneratorType:
        """
        Generate intervals indicating the valid sentences.
        """
        index = -1
        labels = None

        while True:

            # 1. Find the start of the sentence.
            start = -1
            while True:
                # Check the ``labels`` generated from step (2).
                if labels is None:
                    # https://www.python.org/dev/peps/pep-0479/
                    try:
                        index, labels = next(self.index_labels_generator)
                    except StopIteration:
                        return
                # Check if we found a valid sentence char.
                if labels[SentenceValidCharacterLabeler]:
                    start = index
                    break
                # Trigger next(...) action.
                labels = None
                index = -1

            # 2. Find the ending.
            end = -1
            try:
                while True:
                    index, labels = next(self.index_labels_generator)
                    print(index)

                    # Detected invalid char.
                    if not labels[SentenceValidCharacterLabeler] and not labels[WhitespaceLabeler]:
                        end = index
                        break

                    # Detected sentence ending.
                    if self._labels_indicate_sentence_ending(labels):
                        # Consume the ending span.
                        while True:
                            index, labels = next(self.index_labels_generator)
                            if not self._labels_indicate_sentence_ending(labels):
                                end = index
                                break
                        # yeah we found the ending.
                        break
            except StopIteration:
                end = len(self.input_sequence)
                # Trigger next(...) action.
                labels = None
                index = -1

            yield start, end


SentenceRetType = Tuple[str, workflow.IntervalType]
SentSegLazyRetType = Generator[SentenceRetType, None, None]
SentSegRetType = List[SentenceRetType]


# To make type checking happy.
class _SentenceSegementationOutputGeneratorLazy(workflow.BasicOutputGenerator):

    def _result(self) -> SentSegLazyRetType:
        return ((self.input_sequence[start:end], (start, end))
                for start, end in self.label_processor_result)

    def result(self) -> Any:
        raise NotImplementedError()


class SentenceSegementationOutputGeneratorLazy(_SentenceSegementationOutputGeneratorLazy):

    def result(self) -> SentSegLazyRetType:
        return self._result()


class SentenceSegementationOutputGenerator(_SentenceSegementationOutputGeneratorLazy):

    def result(self) -> SentSegRetType:
        return list(self._result())


def _generate_sentseg_workflow(lazy: bool) -> workflow.BasicWorkflow:
    if lazy:
        output_generator_class = SentenceSegementationOutputGeneratorLazy
    else:
        output_generator_class = SentenceSegementationOutputGenerator

    return workflow.BasicWorkflow(
            sequential_labeler_classes=[
                    SentenceEndingLabeler,
                    CommaLabeler,
                    WhitespaceLabeler,
                    SentenceValidCharacterLabeler,
            ],
            label_processor_class=SentenceSegementationLabelProcessor,
            output_generator_class=output_generator_class,
    )


SENTSEG_WORKFLOW_LAZY = _generate_sentseg_workflow(lazy=True)
SENTSEG_WORKFLOW = _generate_sentseg_workflow(lazy=False)


def _sentseg(sentseg_workflow: workflow.BasicWorkflow, text: str,
             enable_comma_ending: bool = False) -> Union[SentSegLazyRetType, SentSegRetType]:
    config = SentenceSegementationConfig(enable_comma_ending=enable_comma_ending)
    return cast(Union[SentSegLazyRetType, SentSegRetType], sentseg_workflow.result(text, config))


def sentseg(text: str, enable_comma_ending: bool = False) -> SentSegRetType:
    return cast(SentSegRetType, _sentseg(SENTSEG_WORKFLOW, text, enable_comma_ending))


def sentseg_lazy(text: str, enable_comma_ending: bool = False) -> SentSegLazyRetType:
    return cast(SentSegLazyRetType, _sentseg(SENTSEG_WORKFLOW_LAZY, text, enable_comma_ending))
