from pathlib import Path


def is_python_file(path: Path) -> bool:
    return path.is_file() and path.suffix == ".py"


def parse_python_file_tree_from_paths(
    paths: list[Path], ignored_directories: set[str]
) -> list[Path]:
    python_files = []
    for p in paths:
        python_files.extend(parse_python_file_tree(p, ignored_directories))
    return python_files


def parse_python_file_tree(
    root_path: Path, ignored_directories: set[str]
) -> list[Path]:
    """Given a pathlib path, returns a list of all files in the directory recursively

    Args:
        root_path (Path): Root path to a file or directory

    Returns:
        list[Path]: A list of all `.py` files.
    """
    if is_python_file(root_path):
        return [root_path]

    file_list = []
    if root_path.is_dir() and root_path.name not in ignored_directories:
        for item in root_path.iterdir():
            file_list.extend(parse_python_file_tree(item, ignored_directories))

    return file_list
