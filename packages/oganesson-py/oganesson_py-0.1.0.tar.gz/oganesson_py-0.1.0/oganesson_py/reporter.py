from typing import Callable, Optional

from .analysis import MultiFileResults


def output_report(results: MultiFileResults, printer: Optional[Callable] = None):
    if not printer:
        printer = print

    printer("===== Analysis Report =====")
    for file_result in results:
        printer(f"{file_result.file_name}:")
        for r in file_result.results:
            printer(f"\t{r.pretty()}")
