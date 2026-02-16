# -------------------------------------------
# Confidence + Severity Scoring Layer
# -------------------------------------------

def compute_severity_and_confidence(merged_data):
    """
    Adds severity_level and confidence_score to each observation.
    This is deterministic (no LLM needed).
    """

    scored = []

    for item in merged_data:

        issue = str(item.get("inspection_issue", "")).lower()
        thermal = str(item.get("thermal_finding", "")).lower()
        conflict = item.get("conflict", False)

        # -------------------------
        # Severity Rules
        # -------------------------
        severity = "Low"
        score = 0.5
        reason = []

        if "crack" in issue or "leak" in issue:
            severity = "High"
            score += 0.2
            reason.append("Structural keyword detected")

        if "damp" in issue:
            severity = "Medium"
            score += 0.1
            reason.append("Moisture-related issue")

        if "hot" in thermal or "high" in thermal:
            severity = "High"
            score += 0.2
            reason.append("Thermal anomaly detected")

        if conflict:
            score -= 0.2
            reason.append("Conflict between reports")

        # Clamp score between 0 and 1
        score = max(0.0, min(score, 1.0))

        # Add results
        new_item = dict(item)
        new_item["severity_level"] = severity
        new_item["confidence_score"] = round(score, 2)
        new_item["reasoning_note"] = ", ".join(reason) if reason else "Rule-based assessment"

        scored.append(new_item)

    return scored
