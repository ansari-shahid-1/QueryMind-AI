import ollama

from backend.services.prompt_builder import build_sql_prompt


class AIService:
    def __init__(self, model="qwen2.5:3b"):
        self.model = model

    def generate_sql(self, question, schema_context):
        prompt = build_sql_prompt(question, schema_context)

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        sql = response.message.content.strip()

        if sql.startswith("```"):
            sql = sql.split("\n", 1)[1]

        if sql.endswith("```"):
            sql = sql[:-3]

        return sql.strip()