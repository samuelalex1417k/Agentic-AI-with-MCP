from server.tools.project import get_project_files

from server.skills.detect_django import detect_django
from server.skills.security_skill import security_scan
from server.skills.api_skill import api_analyze
from server.skills.database_skill import database_analyze


def analyze_project(project_path: str):

    print("Starting project analysis...")


    report = {
        "project": project_path,
        "framework": None,
        "analysis": {}
    }


    print("Scanning project...")

    project_data = get_project_files(
        project_path
    )


    print("Detecting framework...")


    django_result = detect_django(
        project_data
    )


    report["framework"] = django_result



    if django_result["framework"] == "Django":

        print(
            "Django detected"
        )


        print(
            "Running API analysis..."
        )

        report["analysis"]["api"] = api_analyze(
            project_data
        )


        print(
            "Running database analysis..."
        )

        report["analysis"]["database"] = database_analyze(
            project_data
        )


    print(
        "Running security scan..."
    )


    report["analysis"]["security"] = security_scan(
        project_data
    )


    print(
        "Analysis completed."
    )


    return report