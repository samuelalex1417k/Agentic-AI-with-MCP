from pathlib import Path
import re


IGNORE = {
    "venv",
    ".venv",
    "__pycache__",
    "node_modules",
    ".git"
}


def database_analyze(project_data: dict):

    root = Path(project_data["root"])

    result = {
        "database": None,
        "models_found": 0,
        "models": []
    }


    # Detect database type

    for file in root.rglob("*"):

        if file.name.endswith(".sqlite3"):
            result["database"] = "SQLite"


        if file.name == "settings.py":

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if "postgresql" in content.lower():
                    result["database"] = "PostgreSQL"

                elif "mysql" in content.lower():
                    result["database"] = "MySQL"

            except:
                pass



    # Analyze Django models

    for file in root.rglob("models.py"):

        if any(
            ignored in file.parts
            for ignored in IGNORE
        ):
            continue


        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        except:
            continue



        classes = re.findall(
            r"class\s+(\w+)\(.*models.Model.*\):",
            content
        )


        for model in classes:

            model_data = {
                "name": model,
                "fields": [],
                "relationships": []
            }


            # Get field definitions

            model_block = content[
                content.find(
                    "class " + model
                ):
            ]


            fields = re.findall(
                r"(\w+)\s*=\s*models\.(\w+)",
                model_block
            )


            for field, field_type in fields:

                model_data["fields"].append(
                    field
                )


                if field_type in [
                    "ForeignKey",
                    "OneToOneField",
                    "ManyToManyField"
                ]:

                    model_data["relationships"].append(
                        field_type
                    )



            result["models"].append(
                model_data
            )


            result["models_found"] += 1



    return {
        "database_analysis": result
    }