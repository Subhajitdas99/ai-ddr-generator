import re

# -----------------------------------
# Basic Rule-Based Inspection Parser
# -----------------------------------
def fallback_extract_inspection(text):

    observations = []
    lines = text.split("\n")

    for line in lines:
        if "damp" in line.lower() or "crack" in line.lower() or "leak" in line.lower():
            observations.append({
                "area": "Not Available",
                "issue": line.strip(),
                "evidence": line.strip(),
                "severity_hint": "Not Available"
            })

    if not observations:
        observations.append({
            "area": "Not Available",
            "issue": "Not Available",
            "evidence": "No clear issues detected",
            "severity_hint": "Not Available"
        })

    return observations


# -----------------------------------
# Thermal Rule-Based Parser
# -----------------------------------
def fallback_extract_thermal(text):

    findings = []
    lines = text.split("\n")

    for line in lines:
        if "temp" in line.lower() or "thermal" in line.lower() or "hot" in line.lower():
            findings.append({
                "area": "Not Available",
                "thermal_observation": line.strip(),
                "temperature_note": line.strip(),
                "risk_indicator": "Not Available"
            })

    if not findings:
        findings.append({
            "area": "Not Available",
            "thermal_observation": "Not Available",
            "temperature_note": "Not Available",
            "risk_indicator": "Not Available"
        })

    return findings


# -----------------------------------
# Template-Based DDR Generator
# -----------------------------------
def fallback_generate_ddr(merged_data):

    report = f"""
# Detailed Diagnostic Report (Offline Mode)

## 1. Property Issue Summary
Issues detected based on rule-based analysis.

## 2. Area-wise Observations
{merged_data}

## 3. Probable Root Cause
Not Available

## 4. Severity Assessment
Not Available

## 5. Recommended Actions
Further professional inspection recommended.

## 6. Additional Notes
Generated using offline fallback mode.

## 7. Missing or Unclear Information
Some structured reasoning unavailable due to offline mode.
"""

    return report
