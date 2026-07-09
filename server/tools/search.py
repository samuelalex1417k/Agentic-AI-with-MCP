from pathlib import Path
from typing import Dict, List


DEFAULT_IGNORED_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "media",
    "staticfiles",
}


def search_files(
    project_root: str,
    query: str,
    search_content: bool = False,
    file_extensions: List[str] | None = None,
) -> Dict:
    """
    Search files by filename or file content.

    Args:
        project_root:
            Root project directory.

        query:
            Text to search for.

        search_content:
            If False, search filenames.
            If True, search inside files.

        file_extensions:
            Optional list of extensions.
            Example:
            [".py", ".txt"]

    Returns:
        Dictionary containing search results.
    """

    root = Path(project_root).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"{project_root} does not exist."
        )

    results = []

    for path in root.rglob("*"):

        # Skip ignored folders
        if any(part in DEFAULT_IGNORED_DIRS for part in path.parts):
            continue

        if not path.is_file():
            continue

        # Extension filter
        if file_extensions:
            if path.suffix not in file_extensions:
                continue

        relative_path = str(path.relative_to(root))

        # -------------------------
        # Filename search
        # -------------------------
        if not search_content:

            if query.lower() in path.name.lower():

                results.append(
                    {
                        "file": relative_path,
                        "match": path.name,
                        "type": "filename",
                    }
                )

        # -------------------------
        # Content search
        # -------------------------
        else:

            try:
                with open(
                    path,
                    "r",
                    encoding="utf-8",
                ) as file:

                    for line_number, line in enumerate(file, start=1):

                        if query.lower() in line.lower():

                            results.append(
                                {
                                    "file": relative_path,
                                    "line": line_number,
                                    "content": line.strip(),
                                    "type": "content",
                                }
                            )

            except (UnicodeDecodeError, PermissionError):
                continue

    return {
        "query": query,
        "matches": len(results),
        "results": results,
    }