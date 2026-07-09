from typing import Dict


def detect_django(project: Dict) -> Dict:
    """
    Detect whether the scanned project is a Django project.
    """

    files = project.get("files", [])
    apps = project.get("python_apps", [])

    indicators = {
        "manage.py": False,
        "settings.py": False,
        "urls.py": False,
        "django_apps": []
    }

    # -----------------------
    # Root files
    # -----------------------

    for file in files:

        name = file.get("name", "")

        if name == "manage.py":
            indicators["manage.py"] = True

        elif name == "settings.py":
            indicators["settings.py"] = True

        elif name == "urls.py":
            indicators["urls.py"] = True

    # -----------------------
    # Django Apps
    # -----------------------

    for app in apps:

        required = [
            "models.py",
            "views.py",
            "apps.py"
        ]

        app_files = app.get("files", [])

        if all(item in app_files for item in required):

            indicators["django_apps"].append(
                app["name"]
            )

    # -----------------------
    # Score
    # -----------------------

    score = 0

    if indicators["manage.py"]:
        score += 40

    if indicators["settings.py"]:
        score += 30

    if indicators["urls.py"]:
        score += 20

    if indicators["django_apps"]:
        score += 10

    return {
        "framework": "Django" if score >= 50 else "Unknown",
        "confidence": score,
        "summary": {
            "total_apps": len(indicators["django_apps"]),
            "has_models": len(indicators["django_apps"]) > 0,
            "has_serializers": any(
                "serializers.py" in app.get("files", [])
                for app in apps
            ),
            "has_api_routes": any(
                "urls.py" in app.get("files", [])
                for app in apps
            )
        },
        "apps": indicators["django_apps"]
    }