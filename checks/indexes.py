def collect_indexes(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.name AS schema_name,
            t.name AS table_name,
            i.name AS index_name,
            i.type_desc AS index_type,
            i.is_unique,
            i.is_primary_key,
            i.is_disabled
        FROM sys.indexes AS i
        INNER JOIN sys.tables AS t
            ON i.object_id = t.object_id
        INNER JOIN sys.schemas AS s
            ON t.schema_id = s.schema_id
        WHERE i.index_id > 0
        ORDER BY
            s.name,
            t.name,
            i.index_id;
    """)

    rows = cursor.fetchall()

    return [
        {
            "schema_name": row.schema_name,
            "table_name": row.table_name,
            "index_name": row.index_name,
            "index_type": row.index_type,
            "is_unique": bool(row.is_unique),
            "is_primary_key": bool(row.is_primary_key),
            "is_disabled": bool(row.is_disabled)
        }
        for row in rows
    ]