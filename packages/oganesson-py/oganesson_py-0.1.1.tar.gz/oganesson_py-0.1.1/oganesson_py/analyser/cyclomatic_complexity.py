from __future__ import annotations

from typing import Optional
from pydantic import BaseModel

from colorama import Fore

from radon.complexity import cc_visit
from radon.visitors import Function

from .analyser import Analyser, Result


class CCAnalyser:
    def __init__(
        self,
        threshold: Optional[int] = None,
        next_analyser: Optional[Analyser] = None,
    ):
        self.next = next_analyser
        self.threshold = threshold if threshold else 0

    def set_next(self, next_analyser: Analyser):
        self.next = next_analyser

    def __call__(self, file: str) -> list[Result]:
        other_results = self.next(file) if self.next else []

        results = cc_visit(file)
        for r in results:
            if isinstance(r, Function) and r.complexity > self.threshold:
                other_results.append(CCResult.from_result(r))

        return other_results


class CCResult(BaseModel):
    function_name: str
    line_from: int
    line_to: int
    cyclomatic_complexity: int
    class_name: str | None

    def pretty(self) -> str:
        return (
            f"{self.line_from}-{self.line_to}, "
            f"{self.resolved_function_name} - Cyclomatic Complexity"
            f" = {self.pretty_cyclomatic_complexity}"
        )

    @property
    def pretty_cyclomatic_complexity(self) -> str:
        match self.cyclomatic_complexity:
            case num if num <= 5:
                return f"{Fore.GREEN}{num}{Fore.RESET}"
            case num if 5 < num <= 10:
                return f"{Fore.YELLOW}{num}{Fore.RESET}"
            case num if 10 < num:
                return f"{Fore.RED}{num}{Fore.RESET}"

    @property
    def resolved_function_name(self) -> str:
        return (
            f"{self.class_name}.{self.function_name}"
            if self.class_name
            else self.function_name
        )

    @classmethod
    def from_result(cls, result: Function) -> CCResult:
        return CCResult(
            function_name=result.name,
            line_from=result.lineno,
            line_to=result.endline,
            cyclomatic_complexity=result.complexity,
            class_name=result.classname,
        )
