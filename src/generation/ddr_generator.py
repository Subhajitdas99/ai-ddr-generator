from openai import OpenAI
import json

# Offline fallback
from src.reasoning.offline_fallback import fallback_generate_ddr

client = OpenAI()

# -----------------------------
# Helper: Clean JSON-like input
# -----------------------------
def serialize_data(data):
    """
    Convert structured observations into clean JSON string.
    Ensures consistent formatting before sending to LLM.
    """
    try:
        return json.dumps(data, indent=2)
    except Exception:
        return str(data)


# ------------------------------------
# Guardrail Prompt Builder (IMPORTANT)
# ------------------------------------
def build_ddr_messages(structured_data, base_prompt):
    """
    Builds strict system + user messages.
    Adds anti-hallucination rules automatically.
    """

    guardrail_rules = """
STRICT VALIDATION RULES:

1. NEVER invent information.
2. Use ONLY the provided structured data.
3. If a field is missing → write "Not Available".
4. If conflict = true → explicitly mention the conflict.
5. Do NOT add engineering assumptions.
6. Use simple client-friendly language.
7. Do NOT output JSON — write a readable report.
"""

    system_message = base_prompt + "\n" + guardrail_rules

    user_message = f"""
STRUCTURED OBSERVATION DATA:
{serialize_data(structured_data)}

Generate the final Detailed Diagnostic Report.
"""

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]


# ------------------------------
# DDR Generator (Main Function)
# ------------------------------
def generate_ddr(structured_data, prompt):
    """
    Generates final DDR report from merged structured observations.
    Falls back to offline generator if API fails.
    """

    try:
        messages = build_ddr_messages(structured_data, prompt)

        response = client.chat.completions.create(
            model="gpt-5-mini",
            temperature=0.2,
            messages=messages
        )

        report = response.choices[0].message.content

        # -------- Safety Check ----------
        if not report or len(report.strip()) < 50:
            raise ValueError("DDR output too short — possible generation failure.")

        return report

    except Exception as e:
        print("⚠️ Switching to OFFLINE DDR generation:", e)
        return fallback_generate_ddr(structured_data)

