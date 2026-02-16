from openai import OpenAI
import json

# Offline fallback
from src.reasoning.offline_fallback import fallback_extract_inspection

client = OpenAI()


def safe_json_loads(content: str):
    """
    Safely parse JSON even if model adds extra text.
    """
    try:
        return json.loads(content)
    except Exception:
        start = content.find("[")
        end = content.rfind("]") + 1
        return json.loads(content[start:end])


def extract_inspection(text, prompt):
    """
    Extract structured inspection observations.
    Uses LLM first, falls back to offline parser if API fails.
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
            raise ValueError("Inspection extraction must return a list.")

        return data

    except Exception as e:
        print("⚠️ Switching to OFFLINE inspection fallback:", e)
        return fallback_extract_inspection(text)


