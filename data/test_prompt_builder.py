from backend.services.prompt_builder import build_sql_prompt
from backend.services.schema_context import get_schema_context


schema = get_schema_context()

question = "What are the top 5 product categories by total sales?"

prompt = build_sql_prompt(question, schema)

print(prompt)