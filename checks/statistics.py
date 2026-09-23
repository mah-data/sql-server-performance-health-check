def collect_statistics(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.name AS schema_name,
            t.name AS table_name,
            st.name AS statistics_name,
            sp.last_updated,
            sp.rows,
            sp.rows_sampled,
            sp.modification_counter
        FROM sys.stats AS st
        INNER JOIN sys.tables AS t
            ON st.object_id = t.object_id
        INNER JOIN sys.schemas AS s
            ON t.schema_id = s.schema_id
        CROSS APPLY sys.dm_db_stats_properties(
            st.object_id,
            st.stats_id
        ) AS sp
        ORDER BY
            s.name,
            t.name,
            st.name;
    """)

    rows = cursor.fetchall()

    return [
        {
            "schema_name": row.schema_name,
            "table_name": row.table_name,
            "statistics_name": row.statistics_name,
            "last_updated": (
                row.last_updated.isoformat()
                if row.last_updated
                else None
            ),
            "rows": row.rows,
            "rows_sampled": row.rows_sampled,
            "modification_counter": row.modification_counter
        }
        for row in rows
    ]