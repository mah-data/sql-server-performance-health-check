import json

from src.connection import get_connection
from checks.environment import collect_environment
from checks.query_performance import collect_query_performance
from assessment.environment_assessment import analyze_environment
from assessment.environment_findings import build_environment_findings
from assessment.query_performance_assessment import analyze_query_performance
from assessment.query_performance_findings import build_query_performance_findings
from checks.wait_statistics import collect_wait_statistics
from assessment.wait_statistics_assessment import analyze_wait_statistics
from assessment.wait_statistics_findings import build_wait_statistics_findings
from checks.blocking import collect_blocking
from checks.indexes import collect_indexes
from assessment.index_assessment import analyze_indexes
from checks.statistics import collect_statistics
from assessment.statistics_assessment import analyze_statistics
from assessment.statistics_findings import build_statistics_findings
from src.report_generator import generate_report


SERVER = "CEO"
DATABASE = "JoinOptimizationLab"
USERNAME = "sa"
PASSWORD = "Mahtab5490"


connection = get_connection(
    SERVER,
    DATABASE,
    USERNAME,
    PASSWORD
)

# 1. Environment
environment = collect_environment(connection)

with open(
    "evidence/environment.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        environment,
        file,
        indent=4,
        ensure_ascii=False
    )

assessment = analyze_environment()

with open(
    "reports/environment_assessment.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        assessment,
        file,
        indent=4,
        ensure_ascii=False
    )

findings = build_environment_findings(assessment)

with open(
    "reports/environment_findings.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        findings,
        file,
        indent=4,
        ensure_ascii=False
    )

# 2. Query Performance
query_performance = collect_query_performance(connection)

with open(
    "evidence/query_performance.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        query_performance,
        file,
        indent=4,
        ensure_ascii=False
    )

query_performance_analysis = analyze_query_performance(
    query_performance
)

query_performance_findings = build_query_performance_findings(
    query_performance_analysis
)

with open(
    "reports/query_performance_assessment.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        query_performance_analysis,
        file,
        indent=4,
        ensure_ascii=False
    )

with open(
    "reports/query_performance_findings.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        query_performance_findings,
        file,
        indent=4,
        ensure_ascii=False
    )

wait_statistics = collect_wait_statistics(connection)
wait_statistics_analysis = analyze_wait_statistics(
    wait_statistics
)

wait_statistics_findings = build_wait_statistics_findings(
    wait_statistics_analysis
)


# 4. Blocking
blocking = collect_blocking(connection)

with open(
    "evidence/blocking.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        blocking,
        file,
        indent=4,
        ensure_ascii=False
    )



# 5. Indexes
indexes = collect_indexes(connection)
indexes_analysis = analyze_indexes(indexes)

with open(
    "evidence/indexes.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        indexes,
        file,
        indent=4,
        ensure_ascii=False
    )

with open(
    "reports/index_assessment.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        indexes_analysis,
        file,
        indent=4,
        ensure_ascii=False
    )

# 6. Statistics
statistics = collect_statistics(connection)

with open(
    "evidence/statistics.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        statistics,
        file,
        indent=4,
        ensure_ascii=False
    )

statistics_analysis = analyze_statistics(statistics)

with open(
    "reports/statistics_assessment.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        statistics_analysis,
        file,
        indent=4,
        ensure_ascii=False
    )

statistics_findings = build_statistics_findings(
    statistics_analysis
)

with open(
    "reports/statistics_findings.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        statistics_findings,
        file,
        indent=4,
        ensure_ascii=False
    )

connection.close()





with open(
    "evidence/wait_statistics.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        wait_statistics,
        file,
        indent=4,
        ensure_ascii=False
    )

with open(
    "reports/wait_statistics_assessment.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        wait_statistics_analysis,
        file,
        indent=4,
        ensure_ascii=False
    )

with open(
    "reports/wait_statistics_findings.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        wait_statistics_findings,
        file,
        indent=4,
        ensure_ascii=False
    )

print("Health check completed.")
print("Evidence and assessments saved.")
generate_report()

print("HTML report generated.")