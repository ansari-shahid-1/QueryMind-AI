from backend.services.query_pipeline import QueryPipeline


pipeline = QueryPipeline()

question = "Which 5 states have the highest number of customers?"
response = pipeline.run(question)

print("\nQuestion:")
print(response["question"])

print("\nGenerated SQL:")
print(response["sql"])

print("\nQuery Results:")
print(response["result"])