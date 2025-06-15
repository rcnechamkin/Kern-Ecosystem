import openai
openai.api_key = "your-real-api-key"

models = openai.models.list()
for model in models.data:
    print(model.id)
