def build_query_performance_findings(queries):
    findings = []

    for query in queries:
        query_text = query["query_text"].strip().lower()

        # Metadata / system queries are not treated as customer findings.
        if "sys." in query_text or "sp_datatype_info" in query_text:
            continue

        if query["avg_cpu_time"] >= 100:
            findings.append({
                "title": "High CPU Query",
                "severity": "High",
                "evidence": query,
                "recommendation": (
                    "Investigate execution plan, query shape, "
                    "indexes, and statistics."
                )
            })

    return findings