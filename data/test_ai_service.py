from backend.services.ai_service import AIService
from backend.services.schema_context import get_schema_context


ai_service = AIService()

schema_context = get_schema_context()

question = "What are the top 5 product categories by total sales?"

sql = ai_service.generate_sql(question, schema_context)

print("\nGenerated SQL:\n")
print(sql)