IGNORED_WAITS = {
    "SQLTRACE_INCREMENTAL_FLUSH_SLEEP",
    "QDS_PERSIST_TASK_MAIN_LOOP_SLEEP",
    "QDS_ASYNC_QUEUE",
    "SP_SERVER_DIAGNOSTICS_SLEEP",
    "PWAIT_EXTENSIBILITY_CLEANUP_TASK",
    "HADR_FILESTREAM_IOMGR_IOCOMPLETION",
    "PREEMPTIVE_XE_GETTARGETSTATE",
    "PREEMPTIVE_XE_CALLBACKEXECUTE",
    "PWAIT_ALL_COMPONENTS_INITIALIZED",
    "STARTUP_DEPENDENCY_MANAGER",
    "MEMORY_ALLOCATION_EXT",
    "CHKPT",
}


def build_wait_statistics_findings(wait_statistics):
    findings = []

    for wait in wait_statistics:
        wait_type = wait["wait_type"]

        if wait_type in IGNORED_WAITS:
            continue

        if wait["wait_percentage"] >= 5:
            findings.append({
                "title": f"Significant Wait Type: {wait_type}",
                "severity": "Review",
                "evidence": wait,
                "recommendation": (
                    "Investigate the workload and resource associated "
                    "with this wait before applying any tuning change."
                )
            })

    return findings