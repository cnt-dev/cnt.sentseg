from cnt.rulebase.sentence_segmenter_next import (
        SentenceEndingLabeler,
        WhitespaceLabeler,
        SentenceValidCharacterLabeler,
)


def test_sentence_ending_labler():
    text = "1。2。”3"
    labeler = SentenceEndingLabeler(text)
    result = [labeler.label(idx) for idx in range(len(text))]
    assert [
            False,
            True,
            False,
            True,
            True,
            False,
    ] == result


def test_whitespace_labeler():
    text = '1 2\t3'
    labeler = WhitespaceLabeler(text)
    result = [labeler.label(idx) for idx in range(len(text))]
    assert [
            False,
            True,
            False,
            True,
            False,
    ] == result


def test_sentence_valid_character_labeler():
    text = '测试 test 123 !!!'
    labeler = SentenceValidCharacterLabeler(text)
    result = [labeler.label(idx) for idx in range(len(text))]
    assert [
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
    ] == result
