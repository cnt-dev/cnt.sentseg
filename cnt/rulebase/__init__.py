# -*- coding: utf-8 -*-
# flake8: noqa

"""Top-level package for cnt.rulebase."""

__author__ = """Hunt Zhan"""
__email__ = 'huntzhan.dev@gmail.com'
__version__ = '0.5.0'


from .sentseg import sentseg
from .dlmseg import dlmseg
from .replace import (
    replace_chinese_chars,
    replace_english_chars,
    replace_digits,
    replace_delimiters,
)