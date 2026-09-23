def collect_wait_statistics(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT TOP 20
            wait_type,
            waiting_tasks_count,
            wait_time_ms,
            signal_wait_time_ms
        FROM sys.dm_os_wait_stats
        WHERE wait_type NOT IN (
            'BROKER_EVENTHANDLER',
            'BROKER_RECEIVE_WAITFOR',
            'BROKER_TASK_STOP',
            'BROKER_TO_FLUSH',
            'BROKER_TRANSMITTER',
            'CHECKPOINT_QUEUE',
            'CLR_AUTO_EVENT',
            'CLR_MANUAL_EVENT',
            'DIRTY_PAGE_POLL',
            'DISPATCHER_QUEUE_SEMAPHORE',
            'FT_IFTS_SCHEDULER_IDLE_WAIT',
            'LAZYWRITER_SLEEP',
            'LOGMGR_QUEUE',
            'ONDEMAND_TASK_QUEUE',
            'REQUEST_FOR_DEADLOCK_SEARCH',
            'SLEEP_TASK',
            'SOS_WORK_DISPATCHER',
            'SQLTRACE_BUFFER_FLUSH',
            'WAITFOR',
            'XE_DISPATCHER_WAIT',
            'XE_TIMER_EVENT'
        )
        ORDER BY wait_time_ms DESC;
    """)

    rows = cursor.fetchall()

    return [
        {
            "wait_type": row.wait_type,
            "waiting_tasks_count": row.waiting_tasks_count,
            "wait_time_ms": row.wait_time_ms,
            "signal_wait_time_ms": row.signal_wait_time_ms
        }
        for row in rows
    ]