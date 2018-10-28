"""
Shared type annotations.
"""
from typing import Generator, Tuple, List

IntervalType = Tuple[int, int]
IntervalGeneratorType = Generator[IntervalType, None, None]

CommonSentenceType = Tuple[str, IntervalType]
CommonOutputLazyType = Generator[CommonSentenceType, None, None]
CommonOutputType = List[CommonSentenceType]
