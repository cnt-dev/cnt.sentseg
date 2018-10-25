"""
Consts for detecting digit chars.
"""
from cnt.rulebase import utils

#: Digits.
DIGITS = utils.sorted_chain(
        # ASCII_DIGIT_RANGES
        [
                (0x0030, 0x0039),
        ],
        # DIGIT_EXTENSION_RANGES
        [
                (0xFF10, 0xFF19),
        ],
)
