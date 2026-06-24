import requests
import re

# -----------------------------
# OpenRouter API Key
# -----------------------------
OPENROUTER_API_KEY = "your api key"

# Free model
MODEL = "cohere/north-mini-code:free"


def generate_sql(question, table_name, columns):

    prompt = f"""
You are an expert SQL generator.

Table Name:
{table_name}

Columns:
{', '.join(columns)}

User Question:
{question}

Rules:
1. Return ONLY SQL query.
2. No explanation.
3. No markdown.
4. No backticks.
5. Use only given table and columns.
6. Return valid MySQL query.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "SQL Agent"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "max_tokens": 100
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"OpenRouter API Error {response.status_code}: {response.text}"
        )

    data = response.json()

    print("\n========== OPENROUTER RESPONSE ==========")
    print(data)
    print("=========================================\n")

    if "choices" not in data:
        raise Exception(
            f"No choices found.\nResponse:\n{data}"
        )

    message = data["choices"][0]["message"]

    sql_query = message.get("content")

    if not sql_query:
        raise Exception(
            f"Model returned no SQL.\nResponse:\n{data}"
        )

    sql_query = re.sub(
        r"```sql|```",
        "",
        sql_query,
        flags=re.IGNORECASE
    ).strip()

    sql_query = sql_query.rstrip(";")

    return sql_query