from pathlib import Path

import click
from colorama import Fore

from oganesson_py import reporter


from . import validators, exceptions
from .filetree import parse_python_file_tree_from_paths
from .analyser import build_analyser, POSSIBLE_ANALYSERS
from .analysis import run_for_multiple_files


@click.command()
@click.argument("paths", callback=validators.validate_path, nargs=-1)
@click.option(
    "--analysers",
    "-a",
    type=click.Choice(POSSIBLE_ANALYSERS),
    default=POSSIBLE_ANALYSERS,
    show_default=True,
    multiple=True,
    help="Choice of analysers",
)
@click.option(
    "--max-cc",
    default=0,
    show_default=True,
    type=int,
    help="Threshold for cyclomatic complexity reporting.",
)
@click.option(
    "--min-mi",
    default=100.0,
    show_default=True,
    type=float,
    help="Threshold for maintainability index reporting in range [0, 100].",
    callback=validators.validate_maintainability_index,
)
@click.option(
    "--mi-multiline-comments",
    default=True,
    type=bool,
    show_default=True,
    help="Treat multi-line strings as comments for maintainability reporting.",
)
@click.option(
    "--trigger",
    "-t",
    default=False,
    is_flag=True,
    show_default=True,
    type=bool,
    help="Raise an exception if quality thesholds are breached.",
)
@click.option(
    "--ignore",
    multiple=True,
    default=["venv", ".venv", ".git"],
    show_default=True,
    help="Directories to ignore",
)
def main(
    paths: list[Path],
    analysers: list[str],
    max_cc: int,
    min_mi: float,
    mi_multiline_comments: bool,
    trigger: bool,
    ignore: set[str],
):
    """
    # Oganesson

    A CLI for running quality metrics on Python code.  Currently a wrapper
    around Radon, with intent to add a few extra metrics in time.

    Whereas radon has flake8 support, and xenon is designed to work in a CI for
    cyclometric complexity, the maintainability index isn't supported in CI out
    of the box.  This tool produces a report to the stdout of all instances
    which don't satisfy the thresholds set.  If the trigger flag is set, the
    tool will raise an exception (for CI, or in future commit hooks).
    """
    python_files = parse_python_file_tree_from_paths(paths, ignore)

    analyser = build_analyser(
        analysers=analysers,
        max_cc=max_cc,
        min_mi=min_mi,
        mi_multi_as_comments=mi_multiline_comments,
    )

    results = run_for_multiple_files(python_files, analyser)

    reporter.output_report(results=results, printer=click.echo)

    if trigger and results:
        raise exceptions.QualityFailureException(
            f"{Fore.RED}Quality metrics failed across {len(results)} files.{Fore.RESET}"
        )


if __name__ == "__main__":
    main()
