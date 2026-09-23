import json


def analyze_environment():
    with open(
        "evidence/environment.json",
        "r",
        encoding="utf-8"
    ) as file:
        environment = json.load(file)

    return {
        "server_name": environment["server_name"],
        "database_name": environment["database_name"],
        "sql_server_version": environment["sql_server_version"],
        "assessment_time": environment["assessment_time"],
        "status": "OK"
    }