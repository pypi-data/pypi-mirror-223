from __future__ import annotations
from typing import Optional

from oganesson_py.analyser.maintainability_index import MIAnalyser

from .analyser import Analyser, RootAnalyser
from .cyclomatic_complexity import CCAnalyser


POSSIBLE_ANALYSERS = ["cc", "mi"]


def build_analyser(
    analysers: set[str],
    max_cc: int = 0,
    min_mi: float = 100,
    mi_multi_as_comments: bool = True,
):
    builder = AnalyserBuilder()

    if "cc" in analysers:
        builder = builder.add_cc_analyser(threshold=max_cc)
    if "mi" in analysers:
        builder = builder.add_mi_analyser(
            threshold=min_mi, multi_as_comments=mi_multi_as_comments
        )

    return builder.build()


class AnalyserBuilder:
    analyser: Analyser

    def __init__(self):
        self._reset()

    def _reset(self):
        self.analyser = RootAnalyser()

    def add_cc_analyser(
        self,
        threshold: int,
    ) -> AnalyserBuilder:
        cc_analyser = CCAnalyser(threshold=threshold, next_analyser=self.analyser)
        self.analyser = cc_analyser
        return self

    def add_mi_analyser(
        self, threshold: float, multi_as_comments: bool
    ) -> AnalyserBuilder:
        mi_analyser = MIAnalyser(
            threshold=threshold,
            multi_as_comments=multi_as_comments,
            next_analyser=self.analyser,
        )
        self.analyser = mi_analyser
        return self

    def build(self) -> Analyser:
        built_analyser = self.analyser
        self._reset()
        return built_analyser
