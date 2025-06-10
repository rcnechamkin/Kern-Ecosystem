import os
from dotenv import load_dotenv

load_dotenv()  # Reads .env into os.environ

def get_openai_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment.")
    return key
