from typing import List, Optional
import click

from pathlib import Path


def validate_path(ctx, param, value) -> List[Path]:
    paths = list(value) if value else [Path(".")]
    for path in paths:
        if not path.exists():
            raise click.ClickException(
                f"File/directory {value} does not exist. Please enter a valid file path."
            )
    return paths


def validate_maintainability_index(ctx, param, value) -> Optional[float]:
    if value is None:
        return value
    if not 0 <= value <= 100:
        raise click.ClickException(
            f"Maintainability index threshold should be in [0, 100]. Received {value}"
        )
    return float(value)
