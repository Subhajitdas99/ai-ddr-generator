from openai import OpenAI
import json

client = OpenAI()

# ----------------------------------------
# Helper: Serialize structured data safely
# ----------------------------------------
def serialize(data):
    try:
        return json.dumps(data, indent=2)
    except:
        return str(data)


# --------------------------------------------------
# LLM Evaluator — Checks hallucination & rule breaks
# --------------------------------------------------
def evaluate_ddr(structured_data, generated_ddr):
    """
    Evaluates whether the DDR violates rules:
    - hallucinated info
    - missing 'Not Available'
    - ignored conflicts

    Returns:
        dict with evaluation result
    """

    evaluator_prompt = """
You are an AI Safety Evaluator.

Your job is to verify whether the Detailed Diagnostic Report (DDR)
contains information NOT present in the structured data.

VALIDATION RULES:
1. If DDR introduces new facts → mark hallucination=true.
2. If missing data exists but DDR did not write "Not Available" → mark missing_rule_violation=true.
3. If structured data shows conflict=true but DDR does not mention conflict → mark conflict_ignored=true.
4. Be strict and conservative.

Return ONLY JSON:

{
 "hallucination": false,
 "missing_rule_violation": false,
 "conflict_ignored": false,
 "notes": ""
}
"""

    user_message = f"""
STRUCTURED DATA:
{serialize(structured_data)}

DDR OUTPUT:
{generated_ddr}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": evaluator_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        content = response.choices[0].message.content

        # Safe JSON parse
        try:
            return json.loads(content)
        except:
            start = content.find("{")
            end = content.rfind("}") + 1
            return json.loads(content[start:end])

    except Exception as e:
      print("⚠️ Evaluator switched to OFFLINE mode:", e)

    return {
        "hallucination": False,
        "missing_rule_violation": False,
        "conflict_ignored": False,
        "notes": "Offline evaluation mode (LLM unavailable)"
    }

