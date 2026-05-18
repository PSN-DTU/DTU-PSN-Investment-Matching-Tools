import json
from llm_api import puter_chat, clean_json_response

def get_company_structure(company_name, instructions=None, model="openai/gpt-5.2"):
    if instructions is None:
        instructions = (
            "Return structured corporate hierarchy data.\n"
            "Output ONLY valid JSON. No markdown. No explanations.\n"
            "Subsidiaries must contain at least two entries.\n"
        )

    prompt = f"""{instructions}

Company: "{company_name}"

Required JSON format:

{{
    "company": "{company_name}",
    "immediate_parent": {{"name": string or null, "description": string}},
    "ultimate_parent": {{"name": string or null, "description": string}},
    "subsidiaries": [
        {{"name": string, "description": string}},
        {{"name": string, "description": string}}
    ]
}}

Output JSON ONLY.
"""

    try:
        response = puter_chat(prompt, model=model)
        cleaned = clean_json_response(response)
        data = json.loads(cleaned)

        subs = data.get("subsidiaries", [])
        if not isinstance(subs, list) or len(subs) < 2:
            raise ValueError("Model returned fewer than two subsidiaries.")

        return data

    except Exception as e:
        return {"error": str(e), "raw_response": response if 'response' in locals() else None}
