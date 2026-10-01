import sqlglot
from sqlglot import exp


ALLOWED_TABLES = {
    "customers",
    "orders",
    "order_items",
    "payments",
    "order_reviews",
    "products",
    "sellers",
    "geolocation",
    "category_translation",
}

FORBIDDEN_FUNCTIONS = {
    "pg_sleep",
    "set_config",
    "pg_read_file",
    "pg_read_binary_file",
    "pg_ls_dir",
    "lo_import",
    "lo_export",
}


def validate_query(query):
    try:
        statements = sqlglot.parse(query, read="postgres")

        if len(statements) != 1 or statements[0] is None:
            return False, "Only one SQL statement is allowed."

        statement = statements[0]

        if not isinstance(statement, exp.Select):
            return False, "Only SELECT queries are allowed."

        forbidden = (
            exp.Insert,
            exp.Update,
            exp.Delete,
            exp.Drop,
            exp.Create,
            exp.Into,
        )

        for kind in forbidden:
            if next(statement.find_all(kind), None) is not None:
                return False, "The query contains a prohibited operation."

        for table in statement.find_all(exp.Table):
            schema = table.db.lower() if table.db else ""
            table_name = table.name.lower()

            if schema != "analytics" or table_name not in ALLOWED_TABLES:
                return False, "Queries can access only approved analytics tables."

        for function in statement.find_all(exp.Func):
            function_name = getattr(function, "name", "").lower()

            if function_name in FORBIDDEN_FUNCTIONS:
                return False, f"The function '{function_name}' is not allowed."

        return True, "Query is valid."

    except sqlglot.errors.ParseError:
        return False, "Invalid SQL syntax."