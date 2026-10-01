from decimal import Decimal


def calculate_result_facts(result):
    columns = result["columns"]
    rows = result["rows"]

    facts = {
        "row_count": len(rows),
        "columns": columns,
        "numeric_summary": {}
    }

    for index, column in enumerate(columns):
        values = [
            row[index]
            for row in rows
            if isinstance(row[index], (int, float, Decimal))
            and not isinstance(row[index], bool)
        ]

        if values:
            facts["numeric_summary"][column] = {
                "minimum": min(values),
                "maximum": max(values),
                "total": sum(values),
                "average": sum(values) / len(values)
            }

    return facts