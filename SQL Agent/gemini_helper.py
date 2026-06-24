import google.generativeai as genai

genai.configure(
    api_key="your api key "
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

def generate_sql(prompt):
    response = model.generate_content(prompt)
    return response.text