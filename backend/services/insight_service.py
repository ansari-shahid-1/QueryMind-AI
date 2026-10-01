
import ollama

from backend.services.insight_validator import calculate_result_facts


class InsightService:
    def __init__(self, model="qwen2.5:3b"):
        self.model = model

    def generate_insight(self, question, sql, result):
        columns = result["columns"]
        rows = result["rows"]

        if not rows:
            return "No records were found for this question. Try adjusting your query."

        data = [
            dict(zip(columns, row))
            for row in rows
        ]

        facts = calculate_result_facts(result)

        prompt = f"""
You are a data analyst explaining query results to a business user.

Original question:
{question}

SQL query:
{sql}

Actual query results:
{data}

Calculated facts (verified by Python):
{facts}

Your task:
Explain the query results accurately and concisely.

Strict instructions:
- Report only facts directly supported by the actual query results.
- Use the calculated facts as a reference for numerical accuracy.
- Mention relevant numbers from the results.
- Use readable category names when possible.
- For sales or revenue values, use Brazilian reais (R$).
- Do not add currency symbols to values that are not monetary.
- Do not invent percentages, rankings, statistics, or business trends.
- Do not claim that the results represent all records unless the query confirms this.
- Do not make assumptions about business performance or importance.
- Do not use vague phrases such as "significant portion", "majority of total sales", "strong performance", or "highlighting their importance".
- Do not add an unsupported concluding sentence.
- Do not repeat the SQL query.

Output format:
1. Start with one short sentence describing what the query found.
2. List the relevant results with their values.
3. Stop after reporting the results. Do not add a conclusion.

Keep the response concise and easy to understand.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content.strip()
