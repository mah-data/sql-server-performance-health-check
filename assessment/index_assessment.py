def analyze_indexes(indexes):
    analyzed = []

    for index in indexes:
        analyzed.append({
            "schema_name": index["schema_name"],
            "table_name": index["table_name"],
            "index_name": index["index_name"],
            "index_type": index["index_type"],
            "is_unique": index["is_unique"],
            "is_primary_key": index["is_primary_key"],
            "is_disabled": index["is_disabled"],
            "status": "Disabled" if index["is_disabled"] else "Enabled"
        })

    return analyzed