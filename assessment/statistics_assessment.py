def analyze_statistics(statistics):
    analyzed = []

    for stat in statistics:
        rows = stat["rows"]
        rows_sampled = stat["rows_sampled"]
        modification_counter = stat["modification_counter"]

        if rows and rows_sampled:
            sample_percentage = (
                rows_sampled / rows
            ) * 100
        else:
            sample_percentage = None

        analyzed.append({
            "schema_name": stat["schema_name"],
            "table_name": stat["table_name"],
            "statistics_name": stat["statistics_name"],
            "last_updated": stat["last_updated"],
            "rows": rows,
            "rows_sampled": rows_sampled,
            "modification_counter": modification_counter,
            "sample_percentage": (
                round(sample_percentage, 2)
                if sample_percentage is not None
                else None
            )
        })

    return analyzed