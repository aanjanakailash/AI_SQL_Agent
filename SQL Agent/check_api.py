import requests

API_KEY = "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"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(
    "https://openrouter.ai/api/v1/auth/key",
    headers=headers
)

print(response.status_code)
print(response.text)