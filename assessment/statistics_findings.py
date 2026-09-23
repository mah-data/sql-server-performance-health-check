def build_statistics_findings(statistics):
    findings = []

    for stat in statistics:
        if stat["modification_counter"] is None:
            continue

        if (
            stat["rows"]
            and stat["modification_counter"] > 0
        ):
            findings.append({
                "title": "Statistics Have Pending Modifications",
                "severity": "Review",
                "evidence": stat,
                "recommendation": (
                    "Review statistics freshness and determine "
                    "whether an update is required based on workload "
                    "and modification patterns."
                )
            })

    return findings