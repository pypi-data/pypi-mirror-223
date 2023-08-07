from __future__ import annotations

from typing import Optional, Protocol


class Result(Protocol):
    def pretty(self) -> str:
        ...


class Analyser(Protocol):
    def set_next(self, next_analyser: Analyser):
        ...

    def __call__(self, file: str) -> list[Result]:
        ...


class RootAnalyser:
    def __init__(self):
        self.next = None

    def set_next(self, next_analyser: Analyser):
        self.next = next_analyser

    def __call__(self, file: str) -> list[Result]:
        if not self.next:
            return []
        return self.next(file)
