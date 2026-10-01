from backend.services.insight_validator import calculate_result_facts


result = {
    "columns": ["category", "total_sales"],
    "rows": [
        ("health_beauty", 1258681.34),
        ("watches_gifts", 1205005.68),
        ("bed_bath_table", 1036988.68),
        ("sports_leisure", 988048.97),
        ("computers_accessories", 911954.32)
    ]
}

facts = calculate_result_facts(result)

print("Calculated facts:")
print(facts)

assert facts["row_count"] == 5
assert facts["numeric_summary"]["total_sales"]["maximum"] == 1258681.34
assert facts["numeric_summary"]["total_sales"]["minimum"] == 911954.32

print("\nAll validation tests passed!")