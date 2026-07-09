from typing import Dict


def analyze_django_project(
    structure: Dict
) -> Dict:

    apps = structure.get(
        "python_apps",
        []
    )


    has_models = False
    has_serializers = False
    has_urls = False


    app_names = []


    for app in apps:

        app_names.append(
            app["name"]
        )

        files = app["files"]


        if "models.py" in files:
            has_models = True

        if "serializers.py" in files:
            has_serializers = True

        if "urls.py" in files:
            has_urls = True



    score = 0


    if len(apps) > 0:
        score += 40

    if has_models:
        score += 20

    if has_serializers:
        score += 20

    if has_urls:
        score += 20



    return {

        "framework": "Django",

        "confidence": score,

        "summary": {

            "total_apps": len(apps),

            "has_models": has_models,

            "has_serializers": has_serializers,

            "has_api_routes": has_urls

        },

        "apps": app_names

    }