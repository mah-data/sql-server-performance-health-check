def analyze_query_performance(queries):
    analyzed = []

    for query in queries:
        execution_count = query["execution_count"]

        avg_cpu = (
            query["total_cpu_time"] / execution_count
            if execution_count
            else 0
        )

        avg_elapsed = (
            query["total_elapsed_time"] / execution_count
            if execution_count
            else 0
        )

        avg_logical_reads = (
            query["total_logical_reads"] / execution_count
            if execution_count
            else 0
        )

        analyzed.append({
            "execution_count": execution_count,
            "total_cpu_time": query["total_cpu_time"],
            "total_elapsed_time": query["total_elapsed_time"],
            "total_logical_reads": query["total_logical_reads"],
            "total_logical_writes": query["total_logical_writes"],
            "avg_cpu_time": round(avg_cpu, 2),
            "avg_elapsed_time": round(avg_elapsed, 2),
            "avg_logical_reads": round(avg_logical_reads, 2),
            "query_text": query["query_text"]
        })

    return analyzed