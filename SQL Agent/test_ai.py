from openai import OpenAI

client = OpenAI(
    api_key="your api key",
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="cohere/north-mini-code:free",
    messages=[
        {
            "role": "user",
            "content": "Convert 'Top 5 cities by revenue' into SQL query"
        }
    ]
)

print(response.choices[0].message.content)