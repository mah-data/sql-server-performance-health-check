def build_environment_findings(assessment):
    findings = []

    if assessment["status"] != "OK":
        findings.append({
            "title": "Environment assessment failed",
            "severity": "High",
            "evidence": assessment,
            "recommendation": "Review SQL Server connectivity and environment configuration."
        })

    return findings