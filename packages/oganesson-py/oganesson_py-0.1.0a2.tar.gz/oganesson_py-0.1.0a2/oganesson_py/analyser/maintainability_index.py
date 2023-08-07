from __future__ import annotations

from typing import Optional
from pydantic import BaseModel

from colorama import Fore

from radon.metrics import mi_visit

from .analyser import Analyser, Result


class MIAnalyser:
    def __init__(
        self,
        threshold: float,
        multi_as_comments: bool,
        next_analyser: Optional[Analyser] = None,
    ):
        self.next = next_analyser
        self.threshold = threshold
        self.multi_as_comments = multi_as_comments

    def set_next(self, next_analyser: Analyser):
        self.next = next_analyser

    def __call__(self, file: str) -> list[Result]:
        other_results = self.next(file) if self.next else []

        result = mi_visit(file, multi=self.multi_as_comments)
        if result <= self.threshold:
            other_results.append(MIResult(mi=result))

        return other_results


class MIResult(BaseModel):
    mi: float

    def pretty(self) -> str:
        return f"Maintainability Index = {self.pretty_mi}"

    @property
    def pretty_mi(self) -> str:
        match self.mi:
            case num if num >= 40:
                return f"{Fore.GREEN}{num}{Fore.RESET}"
            case num if num >= 20:
                return f"{Fore.YELLOW}{num}{Fore.RESET}"
            case num:
                return f"{Fore.RED}{num}{Fore.RESET}"
