from backend.services.schema_context import get_schema_context


if __name__ == "__main__":
    schema = get_schema_context()

    print(schema)