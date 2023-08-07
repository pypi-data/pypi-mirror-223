from dataclasses import dataclass
from typing import List, Protocol
from pathlib import Path


from .analyser import Analyser, Result


@dataclass
class FileResult:
    file_name: Path
    results: List[Result]


MultiFileResults = List[FileResult]


def run_for_file(file_path: Path, analyser: Analyser) -> FileResult:
    with open(file_path, "r") as f:
        file_contents = f.read()

    analysis = analyser(file_contents)

    return FileResult(file_name=file_path, results=analysis)


def run_for_multiple_files(
    file_paths: List[Path], analyser: Analyser
) -> MultiFileResults:
    results = []
    for file in file_paths:
        result = run_for_file(file, analyser)
        if result.results:
            results.append(result)

    return results
