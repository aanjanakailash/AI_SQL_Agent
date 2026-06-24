from openai import OpenAI

client = OpenAI(
    api_key="your api key",
    base_url="https://openrouter.ai/api/v1"
)

models = client.models.list()

for model in models.data[:50]:
    print(model.id)