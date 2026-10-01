from backend.services.ai_service import AIService
from backend.services.schema_context import get_schema_context
from backend.services.sql_validator import validate_query
from backend.database.query_service import execute_query


class QueryPipeline:
    def __init__(self):
        self.ai_service = AIService()

    def run(self, question):
        schema_context = get_schema_context()

        sql = self.ai_service.generate_sql(
            question,
            schema_context
        )

        is_valid, message = validate_query(sql)

        if not is_valid:
            raise ValueError(
                f"Generated SQL was rejected: {message}"
            )

        result = execute_query(sql)

        return {
            "question": question,
            "sql": sql,
            "result": result
        }