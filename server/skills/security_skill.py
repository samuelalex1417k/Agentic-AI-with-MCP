from pathlib import Path


SENSITIVE_FILES = [
    "serviceAccountKey.json",
    "credentials.json",
    ".env"
]


def security_scan(project_data):

    root = Path(project_data["root"])

    issues = []


    for file in root.rglob("*"):

        if not file.is_file():
            continue


        # Ignore virtual environments
        if "venv" in file.parts:
            continue


        # Check sensitive files
        if file.name in SENSITIVE_FILES:

            issues.append(
                {
                    "severity": "CRITICAL",
                    "file": str(file),
                    "problem":
                    "Sensitive credential file found"
                }
            )


        # Python checks

        if file.suffix == ".py":

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except:
                continue


            if "DEBUG=True" in content:

                issues.append(
                    {
                        "severity":"HIGH",
                        "file":str(file),
                        "problem":
                        "DEBUG=True detected"
                    }
                )


            if "SECRET_KEY" in content:

                issues.append(
                    {
                        "severity":"MEDIUM",
                        "file":str(file),
                        "problem":
                        "Possible exposed SECRET_KEY"
                    }
                )


    return {
        "total_issues":len(issues),
        "issues":issues
    }