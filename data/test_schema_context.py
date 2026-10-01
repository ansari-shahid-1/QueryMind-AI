import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.schema_context import get_schema_context


def main():
    print("Testing schema context...\n")

    context = get_schema_context()

    print(context)

    assert "analytics.order_items.product_id = analytics.products.product_id" in context

    assert (
        "analytics.products.product_category_name = "
        "analytics.category_translation.product_category_name"
    ) in context

    assert "Important JOIN guidance:" in context

    print("\nAll schema context tests passed!")


if __name__ == "__main__":
    main()