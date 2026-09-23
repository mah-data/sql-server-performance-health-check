def collect_query_performance(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT TOP 20
            qs.execution_count,
            qs.total_worker_time,
            qs.total_elapsed_time,
            qs.total_logical_reads,
            qs.total_logical_writes,
            st.text AS query_text
        FROM sys.dm_exec_query_stats AS qs
        CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
        ORDER BY qs.total_worker_time DESC;
    """)

    rows = cursor.fetchall()

    return [
        {
            "execution_count": row.execution_count,
            "total_cpu_time": row.total_worker_time,
            "total_elapsed_time": row.total_elapsed_time,
            "total_logical_reads": row.total_logical_reads,
            "total_logical_writes": row.total_logical_writes,
            "query_text": row.query_text
        }
        for row in rows
    ]