from cnt.rulebase import const

SENTENCE_VALID_CHARS = const.sorted_chain(
        const.ITV_CHINESE_CHARS,
        const.ITV_ENGLISH_CHARS,
        const.ITV_DIGITS,
        const.ITV_DELIMITERS,
)
