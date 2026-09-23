import json
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
EVIDENCE_DIR = BASE_DIR / "evidence"

TEMPLATE_FILE = BASE_DIR / "templates" / "report.html"
OUTPUT_FILE = REPORTS_DIR / "performance_health_check.html"


def load_json(directory, filename):
    path = directory / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_json(data):
    return json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )


def build_environment_html(data):

    if not data:
        return '<p class="empty">No environment data collected.</p>'

    sql_version = data.get(
        "sql_server_version",
        "Unknown"
    ).replace("\n", " ").replace("\t", " ").strip()

    version_number = "Unknown"
    edition = "Unknown"
    operating_system = "Unknown"

    if " - " in sql_version:
        version_number = sql_version.split(" - ", 1)[1].split(" (X64)", 1)[0].strip()

    if "Enterprise Evaluation Edition" in sql_version:
        edition = "Enterprise Evaluation Edition (64-bit)"

    if "on Windows 10 Pro" in sql_version:
        operating_system = "Windows 10 Pro"

    rows = [
        ("Server", data.get("server_name", "Unknown")),
        ("Database", data.get("database_name", "Unknown")),
        ("SQL Server", "Microsoft SQL Server 2022"),
        ("Version", version_number),
        ("Edition", edition),
        ("Operating System", operating_system),
        ("Assessment Time", data.get("assessment_time", "Unknown")),
    ]

    table_rows = []

    for label, value in rows:
        table_rows.append(
            f"""
            <tr>
                <th>{escape(str(label))}</th>
                <td>{escape(str(value))}</td>
            </tr>
            """
        )

    return f"""
    <table>
        <tbody>
            {"".join(table_rows)}
        </tbody>
    </table>
    """

def build_wait_statistics_html(data):

    if not data:
        return '<p class="empty">No wait statistics collected.</p>'

    rows = []

    for wait in data:
        rows.append(
            f"""
            <tr>
                <td>{escape(str(wait.get("wait_type", "Unknown")))}</td>
                <td>{wait.get("waiting_tasks_count", 0):,}</td>
                <td>{wait.get("wait_time_ms", 0):,} ms</td>
                <td>{wait.get("signal_wait_time_ms", 0):,} ms</td>
                <td>{wait.get("wait_percentage", 0):.2f}%</td>
            </tr>
            """
        )

    return f"""
    <table>
        <thead>
            <tr>
                <th>Wait Type</th>
                <th>Waiting Tasks</th>
                <th>Wait Time</th>
                <th>Signal Wait</th>
                <th>Wait %</th>
            </tr>
        </thead>

        <tbody>
            {"".join(rows)}
        </tbody>
    </table>
    """

def build_indexes_html(data):

    if not data:
        return '<p class="empty">No index data collected.</p>'

    rows = []

    for index in data:
        rows.append(
            f"""
            <tr>
                <td>{escape(str(index.get("schema_name", "Unknown")))}</td>
                <td>{escape(str(index.get("table_name", "Unknown")))}</td>
                <td>{escape(str(index.get("index_name", "Unknown")))}</td>
                <td>{escape(str(index.get("index_type", "Unknown")))}</td>
                <td>{"Yes" if index.get("is_unique") else "No"}</td>
                <td>{"Yes" if index.get("is_primary_key") else "No"}</td>
                <td>{"Yes" if index.get("is_disabled") else "No"}</td>
                <td>{escape(str(index.get("status", "Unknown")))}</td>
            </tr>
            """
        )

    return f"""
    <table>
        <thead>
            <tr>
                <th>Schema</th>
                <th>Table</th>
                <th>Index</th>
                <th>Type</th>
                <th>Unique</th>
                <th>Primary Key</th>
                <th>Disabled</th>
                <th>Status</th>
            </tr>
        </thead>

        <tbody>
            {"".join(rows)}
        </tbody>
    </table>
    """

def build_statistics_html(data):

    if not data:
        return '<p class="empty">No statistics data collected.</p>'

    rows = []

    for stat in data:

        last_updated = stat.get("last_updated")

        if last_updated is None:
            last_updated = "N/A"

        rows_count = stat.get("rows")

        if rows_count is None:
            rows_count = "N/A"
        else:
            rows_count = f"{rows_count:,}"

        rows_sampled = stat.get("rows_sampled")

        if rows_sampled is None:
            rows_sampled = "N/A"
        else:
            rows_sampled = f"{rows_sampled:,}"

        modification_counter = stat.get("modification_counter")

        if modification_counter is None:
            modification_counter = "N/A"
        else:
            modification_counter = f"{modification_counter:,}"

        sample_percentage = stat.get("sample_percentage")

        if sample_percentage is None:
            sample_percentage = "N/A"
        else:
            sample_percentage = f"{sample_percentage:.2f}%"

        rows.append(
            f"""
            <tr>
                <td>{escape(str(stat.get("schema_name", "Unknown")))}</td>
                <td>{escape(str(stat.get("table_name", "Unknown")))}</td>
                <td>{escape(str(stat.get("statistics_name", "Unknown")))}</td>
                <td>{escape(str(last_updated))}</td>
                <td>{rows_count}</td>
                <td>{rows_sampled}</td>
                <td>{modification_counter}</td>
                <td>{sample_percentage}</td>
            </tr>
            """
        )

    return f"""
    <table>
        <thead>
            <tr>
                <th>Schema</th>
                <th>Table</th>
                <th>Statistics</th>
                <th>Last Updated</th>
                <th>Rows</th>
                <th>Rows Sampled</th>
                <th>Modification Count</th>
                <th>Sample %</th>
            </tr>
        </thead>

        <tbody>
            {"".join(rows)}
        </tbody>
    </table>
    """

def build_findings_html(findings):

    if not findings:
        return """
        <p class="empty">
            No actionable findings were identified during this assessment.
        </p>
        """

    rows = []

    for finding in findings:

        title = finding.get(
            "title",
            "Unknown Finding"
        )

        severity = finding.get(
            "severity",
            "Review"
        )

        recommendation = finding.get(
            "recommendation",
            "No recommendation provided."
        )

        evidence = finding.get(
            "evidence",
            {}
        )

        rows.append(
            f"""
            <tr>
                <td>{escape(str(title))}</td>
                <td>{escape(str(severity))}</td>
                <td>
                    <pre>{escape(format_json(evidence))}</pre>
                </td>
                <td>{escape(str(recommendation))}</td>
            </tr>
            """
        )

    return f"""
    <table>
        <thead>
            <tr>
                <th>Finding</th>
                <th>Severity</th>
                <th>Evidence</th>
                <th>Recommendation</th>
            </tr>
        </thead>

        <tbody>
            {"".join(rows)}
        </tbody>
    </table>
    """

def build_blocking_html(data):

    if not data:
        return """
        <p class="empty">
            No blocking activity was detected during this assessment.
        </p>
        """

    rows = []

    for blocking in data:

        rows.append(
            f"""
            <tr>
                <td>{escape(str(blocking.get("session_id", "Unknown")))}</td>
                <td>{escape(str(blocking.get("blocking_session_id", "Unknown")))}</td>
                <td>{escape(str(blocking.get("wait_type", "Unknown")))}</td>
                <td>{escape(str(blocking.get("wait_time_ms", "Unknown")))}</td>
            </tr>
            """
        )

    return f"""
    <table>
        <thead>
            <tr>
                <th>Session ID</th>
                <th>Blocking Session</th>
                <th>Wait Type</th>
                <th>Wait Time</th>
            </tr>
        </thead>

        <tbody>
            {"".join(rows)}
        </tbody>
    </table>
    """

def build_query_performance_html(data):

    if not data:
        return '<p class="empty">No query performance data collected.</p>'

    rows = []

    for query in data:
        rows.append(
            f"""
            <tr>
                <td>{query.get("execution_count", 0):,}</td>
                <td>{query.get("total_cpu_time", 0):,} ms</td>
                <td>{query.get("total_elapsed_time", 0):,} ms</td>
                <td>{query.get("total_logical_reads", 0):,}</td>
                <td>{query.get("total_logical_writes", 0):,}</td>
            </tr>
            """
        )

    query_text = escape(
        data[0].get("query_text", "")
    )

    return f"""
    <table>
        <thead>
            <tr>
                <th>Executions</th>
                <th>Total CPU</th>
                <th>Total Elapsed</th>
                <th>Logical Reads</th>
                <th>Logical Writes</th>
            </tr>
        </thead>

        <tbody>
            {"".join(rows)}
        </tbody>
    </table>

    <h3>Query Text</h3>

    <pre>{query_text}</pre>
    """


def generate_report():

    template = TEMPLATE_FILE.read_text(
        encoding="utf-8"
    )

    data = {
        "environment": load_json(
            REPORTS_DIR,
            "environment_assessment.json"
        ),

        "query_performance": load_json(
            EVIDENCE_DIR,
            "query_performance.json"
        ),

        "wait_statistics": load_json(
            REPORTS_DIR,
            "wait_statistics_assessment.json"
        ),

        "indexes": load_json(
            REPORTS_DIR,
            "index_assessment.json"
        ),

        "statistics": load_json(
            REPORTS_DIR,
            "statistics_assessment.json"
        ),

        "environment_findings": load_json(
            REPORTS_DIR,
            "environment_findings.json"
        ),

        "query_performance_findings": load_json(
            REPORTS_DIR,
            "query_performance_findings.json"
        ),

        "wait_statistics_findings": load_json(
            REPORTS_DIR,
            "wait_statistics_findings.json"
        ),

        "statistics_findings": load_json(
            REPORTS_DIR,
            "statistics_findings.json"
        )
    }

    environment_html = build_environment_html(
        data["environment"]
    )

    template = template.replace(
        '<div id="environment"></div>',
        f'<div id="environment">{environment_html}</div>'
    )

    wait_statistics_html = build_wait_statistics_html(
        data["wait_statistics"]
    )

    template = template.replace(
        '<div id="wait-statistics"></div>',
        f'<div id="wait-statistics">{wait_statistics_html}</div>'
    )

    indexes_html = build_indexes_html(
        data["indexes"]
    )

    template = template.replace(
       '<div id="indexes"></div>',
       f'<div id="indexes">{indexes_html}</div>'
    )

    statistics_html = build_statistics_html(
        data["statistics"]
    )

    template = template.replace(
        '<div id="statistics"></div>',
        f'<div id="statistics">{statistics_html}</div>'
    )

    all_findings = (
        data["environment_findings"]
        + data["query_performance_findings"]
        + data["wait_statistics_findings"]
        + data["statistics_findings"]
    )

    findings_html = build_findings_html(
        all_findings
    )

    template = template.replace(
        '<div id="findings"></div>',
        f'<div id="findings">{findings_html}</div>'
    )

    blocking_data = load_json(
        EVIDENCE_DIR,
        "blocking.json"
    )

    blocking_html = build_blocking_html(
        blocking_data
    )

    template = template.replace(
        '<div id="blocking"></div>',
        f'<div id="blocking">{blocking_html}</div>'
    )


    query_html = build_query_performance_html(
        data["query_performance"]
    )

    template = template.replace(
        '<div id="query-performance"></div>',
        f'<div id="query-performance">{query_html}</div>'
    )


    all_findings = (
        data["environment_findings"]
        + data["query_performance_findings"]
        + data["wait_statistics_findings"]
        + data["statistics_findings"]
    )


    database_name = data["environment"].get(
        "database_name",
        "Unknown"
    )

    finding_count = len(all_findings)

    if finding_count == 0:
        status = "No Actionable Findings"
    else:
        status = "Attention Required"


    summary = f"""
    <div class="summary-grid">

        <div class="summary-card">
            <span>Database</span>
            <strong>{escape(database_name)}</strong>
        </div>

        <div class="summary-card">
            <span>Sections Analyzed</span>
            <strong>6</strong>
        </div>

        <div class="summary-card">
            <span>Findings</span>
            <strong>{finding_count}</strong>
        </div>

        <div class="summary-card">
            <span>Status</span>
            <strong>{status}</strong>
        </div>

    </div>
    """


    template = template.replace(
        '<div id="executive-summary"></div>',
        f'<div id="executive-summary">{summary}</div>'
    )


    OUTPUT_FILE.write_text(
        template,
        encoding="utf-8"
    )

    print(
        f"HTML report generated: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    generate_report()