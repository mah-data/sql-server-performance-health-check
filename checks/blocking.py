def collect_blocking(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            r.session_id AS blocked_session_id,
            r.blocking_session_id,
            r.status,
            r.wait_type,
            r.wait_time,
            r.wait_resource,
            DB_NAME(r.database_id) AS database_name,
            t.text AS sql_text
        FROM sys.dm_exec_requests AS r
        OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) AS t
        WHERE r.blocking_session_id <> 0
        ORDER BY r.wait_time DESC;
    """)

    rows = cursor.fetchall()

    return [
        {
            "blocked_session_id": row.blocked_session_id,
            "blocking_session_id": row.blocking_session_id,
            "status": row.status,
            "wait_type": row.wait_type,
            "wait_time_ms": row.wait_time,
            "wait_resource": row.wait_resource,
            "database_name": row.database_name,
            "sql_text": row.sql_text
        }
        for row in rows
    ]