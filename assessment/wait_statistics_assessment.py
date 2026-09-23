def analyze_wait_statistics(wait_statistics):
    analyzed = []

    total_wait_time = sum(
        wait["wait_time_ms"]
        for wait in wait_statistics
    )

    for wait in wait_statistics:
        percentage = (
            (wait["wait_time_ms"] / total_wait_time) * 100
            if total_wait_time
            else 0
        )

        analyzed.append({
            "wait_type": wait["wait_type"],
            "waiting_tasks_count": wait["waiting_tasks_count"],
            "wait_time_ms": wait["wait_time_ms"],
            "signal_wait_time_ms": wait["signal_wait_time_ms"],
            "wait_percentage": round(percentage, 2)
        })

    return analyzed