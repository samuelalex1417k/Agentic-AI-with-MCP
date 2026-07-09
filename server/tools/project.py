from pathlib import Path
from typing import Dict

IGNORE = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "media",
}


def get_project_files(project_path: str) -> Dict:
    """
    Scan a project and return its structure.

    Returns:
    {
        root,
        files,
        directories,
        python_apps
    }
    """

    root = Path(project_path)

    if not root.exists():
        raise FileNotFoundError(f"{project_path} does not exist")

    result = {
        "root": str(root.resolve()),
        "files": [],
        "directories": [],
        "python_apps": []
    }

    # ------------------------
    # Root files & directories
    # ------------------------

    for item in root.iterdir():

        if item.name in IGNORE:
            continue

        if item.is_dir():

            result["directories"].append(item.name)

        else:

            result["files"].append(
                {
                    "name": item.name,
                    "path": str(item),
                    "extension": item.suffix
                }
            )

    # ------------------------
    # Detect Python/Django apps
    # ------------------------

    required = {
        "models.py",
        "views.py",
        "apps.py"
    }

    for directory in result["directories"]:

        folder = root / directory

        if not folder.is_dir():
            continue

        files = [
            f.name
            for f in folder.iterdir()
            if f.is_file()
        ]

        if required.intersection(files):

            result["python_apps"].append(
                {
                    "name": directory,
                    "files": files
                }
            )

    return result


def find_project_config(project_path: str) -> Dict:

    project = get_project_files(project_path)

    configs = {
        "python": False,
        "javascript": False,
        "django": False,
        "docker": False,
        "database": None,
        "files_found": []
    }

    for file in project["files"]:

        name = file["name"].lower()

        if name == "requirements.txt":
            configs["python"] = True
            configs["files_found"].append(name)

        elif name == "package.json":
            configs["javascript"] = True
            configs["files_found"].append(name)

        elif name == "manage.py":
            configs["django"] = True
            configs["files_found"].append(name)

        elif name in ["dockerfile", "docker-compose.yml"]:
            configs["docker"] = True
            configs["files_found"].append(name)

        elif name.endswith(".sqlite3"):
            configs["database"] = "sqlite"

    return configs


def analyze_file(path: str) -> Dict:

    file = Path(path)

    if not file.exists():
        raise FileNotFoundError(path)

    result = {
        "file": file.name,
        "extension": file.suffix,
        "lines": 0,
        "imports": [],
        "classes": [],
        "functions": []
    }

    content = file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    lines = content.splitlines()

    result["lines"] = len(lines)

    for line in lines:

        line = line.strip()

        if line.startswith("import ") or line.startswith("from "):
            result["imports"].append(line)

        elif line.startswith("class "):
            result["classes"].append(line)

        elif line.startswith("def "):
            result["functions"].append(line)

    return result