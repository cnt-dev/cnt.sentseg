"""
Shared type annotations.
"""
from typing import Generator, Tuple

IntervalType = Tuple[int, int]
IntervalGeneratorType = Generator[IntervalType, None, None]
