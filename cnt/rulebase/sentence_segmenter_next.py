from typing import Any, Generator, List, Tuple

import ahocorasick

from cnt.rulebase import workflow
from cnt.rulebase import const


def _build_ac_automation(keys: List[str]) -> Any:
    atm = ahocorasick.Automaton()  # pylint: disable=c-extension-no-member
    for idx, key in enumerate(keys):
        atm.add_word(key, (idx, key))
    atm.make_automaton()
    return atm


def _match_ac_automation(text: str, ac_automation: Any) -> Generator[Tuple[int, int], None, None]:
    prev_start, prev_end = -1, -1

    # ``iter``` will return ``end`` in accending order, see
    # https://github.com/WojciechMula/pyahocorasick/blob/484b1f13549fc9bdeb9868d8a1711d1861f804c3/py/pyahocorasick.py#L229-L252
    # Also note the ``[start, end]`` generated by ``iter`` are closed interval.
    for end, (start, _) in ac_automation.iter(text):
        if prev_start < 0:
            # init.
            prev_start, prev_end = start, end
        elif start <= prev_end + 1:
            # check the interleaved case.
            prev_end = end
        else:
            # should return the previous interval. Note we yield half-opened interval here.
            yield (prev_start, prev_end + 1)
            prev_start, prev_end = start, end

    # yield the last interval.
    if prev_start >= 0:
        yield (prev_start, prev_end + 1)


class SentenceEndingLabeler(workflow.BasicSequentialLabeler):
    AC_AUTOMATION = _build_ac_automation(const.EM_SENTENCE_ENDINGS)

    def label(self, index: int) -> bool:
        pass
