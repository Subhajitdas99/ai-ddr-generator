from openai import OpenAI
import json

# Offline fallback
from src.reasoning.offline_fallback import fallback_extract_thermal

client = OpenAI()


def safe_json_loads(content: str):
    """
    Safely parse JSON even if the model returns extra text.
    """
    try:
        return json.loads(content)
    except Exception:
        start = content.find("[")
        end = content.rfind("]") + 1
        return json.loads(content[start:end])


def extract_thermal(text, prompt):
    """
    Extract structured thermal observations.
    Uses LLM first, switches to offline fallback if API fails.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": prompt + "\nReturn ONLY valid JSON."},
                {"role": "user", "content": text}
            ]
        )

        content = response.choices[0].message.content

        data = safe_json_loads(content)

        if not isinstance(data, list):
            raise ValueError("Thermal extraction must return a list.")

        return data

    except Exception as e:
        print("⚠️ Switching to OFFLINE thermal fallback:", e)
        return fallback_extract_thermal(text)

