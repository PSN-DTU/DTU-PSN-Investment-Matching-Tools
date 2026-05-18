import json
import re
import time
from openai import OpenAI

client = OpenAI()

def puter_chat(prompt, model="openai/gpt-5.2", max_retries=5, delay=1):
    model_map = {
        "openai/gpt-5.2": "gpt-5",
        "openai/gpt-5": "gpt-5"
    }
    actual_model = model_map.get(model, "gpt-5")

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=actual_model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content

        except Exception as e:
            if "rate limit" in str(e).lower() or "429" in str(e):
                wait_time = delay * (2 ** attempt)  # exponential backoff
                print(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

    raise Exception("Max retries exceeded due to rate limits.")


def clean_json_response(response_text):
    if not isinstance(response_text, str) or not response_text:
        return "{}"

    cleaned = re.sub(r"```json\s*", "", response_text)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()