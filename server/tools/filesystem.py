from pathlib import Path
from typing import List, Dict


def list_directory(path: str) -> List[Dict]:
    """
    List files and folders inside a directory.
    """

    directory = Path(path)

    if not directory.exists():
        raise FileNotFoundError(f"'{path}' does not exist.")

    if not directory.is_dir():
        raise NotADirectoryError(f"'{path}' is not a directory.")

    items = []

    for item in sorted(directory.iterdir()):
        items.append(
            {
                "name": item.name,
                "path": str(item.resolve()),
                "type": "directory" if item.is_dir() else "file",
                "extension": item.suffix,
            }
        )

    return items

def read_file(
    project_root: str,
    file_path: str,
    max_lines: int = 200
) -> Dict:
    """
    Read a text file inside the project directory.

    Args:
        project_root:
            The root directory of the project being analyzed.

        file_path:
            The file path relative to the project root.

        max_lines:
            Maximum number of lines to return.

    Returns:
        Dictionary containing file information and content.
    """

    root = Path(project_root).resolve()

    target_file = (root / file_path).resolve()

    # Security check:
    # Make sure the requested file is inside the project folder
    if not str(target_file).startswith(str(root)):
        raise PermissionError(
            "Access denied: file is outside project directory."
        )

    # Check file exists
    if not target_file.exists():
        raise FileNotFoundError(
            f"'{file_path}' does not exist."
        )

    # Check it is actually a file
    if not target_file.is_file():
        raise ValueError(
            f"'{file_path}' is not a file."
        )

    # Read file content
    try:
        with open(
            target_file,
            "r",
            encoding="utf-8"
        ) as file:
            lines = file.readlines()

    except UnicodeDecodeError:
        raise ValueError(
            "File is not a readable text file."
        )

    selected_lines = lines[:max_lines]

    return {
        "file": file_path,
        "absolute_path": str(target_file),
        "lines_returned": len(selected_lines),
        "total_lines": len(lines),
        "truncated": len(lines) > max_lines,
        "content": "".join(selected_lines)
    }