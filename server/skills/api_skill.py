from pathlib import Path


IGNORE = {
    "venv",
    ".venv",
    "__pycache__",
    "node_modules",
    ".git"
}


def api_analyze(project_data: dict):

    result = {
        "total_views": 0,
        "total_serializers": 0,
        "url_files": 0,
        "authentication": None,
        "apps": []
    }


    apps = project_data.get(
        "python_apps",
        []
    )


    for app in apps:

        app_result = {
            "name": app["name"],
            "views": 0,
            "serializers": False,
            "urls": False
        }


        for filename in app.get("files", []):

            # views.py
            if filename == "views.py":

                app_result["views"] = 1

                result["total_views"] += 1



            # serializers.py
            if filename == "serializers.py":

                app_result["serializers"] = True

                result["total_serializers"] += 1



            # urls.py
            if filename == "urls.py":

                app_result["urls"] = True

                result["url_files"] += 1



        result["apps"].append(
            app_result
        )


    return {
        "api_analysis": result
    }