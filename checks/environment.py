from datetime import datetime


def collect_environment(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            @@SERVERNAME AS server_name,
            @@VERSION AS sql_server_version,
            DB_NAME() AS database_name,
            GETDATE() AS assessment_time
    """)

    row = cursor.fetchone()

    return {
        "server_name": row.server_name,
        "sql_server_version": row.sql_server_version,
        "database_name": row.database_name,
        "assessment_time": row.assessment_time.isoformat()
    }