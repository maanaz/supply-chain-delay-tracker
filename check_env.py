import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load .env from the project directory explicitly
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

print("Imports OK")
print("Loaded .env:", env_path)
print("API key loaded:", bool(api_key))
print("Model selected:", repr(model))

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

if not model:
    raise ValueError("GEMINI_MODEL is missing from .env")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=model,
    contents="Reply with exactly: LLM OK",
)

print("Gemini response:", response.text)