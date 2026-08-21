import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=API_KEY)
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")