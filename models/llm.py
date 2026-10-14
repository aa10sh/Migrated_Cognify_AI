import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

def get_api_key() -> str:
    load_dotenv(override=True)
    return os.getenv("OPENAI_API_KEY", "").strip()

def get_model_name() -> str:
    load_dotenv(override=True)
    m = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    return "gpt-4o-mini" if (not m or m == "gpt-5.6-luna") else m

def is_api_key_configured() -> bool:
    key = get_api_key()
    return bool(key and len(key) > 8 and not key.startswith("your_"))


class OpenAIResponsesProxy:
    def parse(self, model: str, input: str, text_format):
        api_key = get_api_key()
        if not api_key or not is_api_key_configured():
            raise ValueError(
                "OPENAI_API_KEY is not configured. Please add your OpenAI API key to the .env file or via Settings."
            )

        model_name = get_model_name() or model
        client_instance = OpenAI(api_key=api_key)

        try:
            return client_instance.responses.parse(
                model=model_name,
                input=input,
                text_format=text_format,
            )
        except Exception as e:
            # Fallback to chat completions parse if responses.parse has SDK compatibility differences
            if hasattr(client_instance.beta.chat.completions, "parse"):
                try:
                    chat_response = client_instance.beta.chat.completions.parse(
                        model=model_name,
                        messages=[{"role": "user", "content": input}],
                        response_format=text_format,
                    )
                    parsed_msg = chat_response.choices[0].message
                    class Wrapper:
                        def __init__(self, p):
                            self.output_parsed = p
                    return Wrapper(parsed_msg.parsed)
                except Exception as inner_e:
                    raise RuntimeError(f"OpenAI API call failed: {inner_e}") from inner_e

            raise RuntimeError(f"OpenAI API call failed: {e}") from e


class OpenAIClientProxy:
    def __init__(self):
        self.responses = OpenAIResponsesProxy()


client = OpenAIClientProxy()
MODEL_NAME = get_model_name()