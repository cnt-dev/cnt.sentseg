# -*- coding: utf-8 -*-
"""Top-level package for cnt.rulebase."""

__author__ = """Hunt Zhan"""
__email__ = 'huntzhan.dev@gmail.com'
__version__ = '0.6.4'

__all__ = [
        'sentseg',
        'sentseg_lazy',
        # 'dlmseg',
        # 'replace_chinese_chars',
        # 'replace_english_chars',
        # 'replace_digits',
        # 'replace_delimiters',
]

from cnt.rulebase.rules import sentseg, sentseg_lazy
# from cnt.rulebase.delimiter_segmenter import dlmseg
# from cnt.rulebase.char_replacer import (
#         replace_chinese_chars,
#         replace_english_chars,
#         replace_digits,
#         replace_delimiters,
# )
