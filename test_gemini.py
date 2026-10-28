import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

print("API key loaded:", bool(api_key))
print("Model:", model)

if not api_key:
    raise ValueError("GEMINI_API_KEY missing from .env")

if not model:
    raise ValueError("GEMINI_MODEL missing from .env")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=model,
    contents="Explain supply chain delays in one sentence."
)

print("\nGemini response:")
print(response.text)