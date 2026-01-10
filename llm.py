from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv('.env')



def call_llm_json(system_prompt, user_prompt) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        store=True,
    )

    text = response.choices[0].message.content

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Helpful debugging info
        raise ValueError(f"Model did not return valid JSON. Raw output:\n{text}") from e