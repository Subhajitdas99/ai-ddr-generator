import os
import json
from src.reasoning.confidence_scoring import compute_severity_and_confidence

# -------------------------
# Imports (your modules)
# -------------------------
from src.ingestion.parser import extract_pdf_text
from src.extraction.extract_inspection import extract_inspection
from src.extraction.extract_thermal import extract_thermal
from src.reasoning.merge_logic import merge_observations
from src.reasoning.evaluator_guardrail import evaluate_ddr
from src.generation.ddr_generator import generate_ddr



# -------------------------
# Helper: Safe File Read
# -------------------------
def load_text_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------
# Helper: Ensure Output Dir
# -------------------------
def ensure_output_folder():
    os.makedirs("outputs", exist_ok=True)


# -------------------------
# Main Pipeline
# -------------------------
def run_pipeline():

    print("🚀 Starting DDR Generation Pipeline...")

    ensure_output_folder()

    # ---- Load Prompts ----
    inspection_prompt = load_text_file("prompts/inspection_prompt.txt")
    thermal_prompt = load_text_file("prompts/thermal_prompt.txt")
    ddr_prompt = load_text_file("prompts/ddr_prompt.txt")

    # ---- Extract PDF Text ----
    inspection_path = "data/inspection_report.pdf"
    thermal_path = "data/thermal_report.pdf"

    inspection_text = extract_pdf_text(inspection_path)
    thermal_text = extract_pdf_text(thermal_path)

    print("📄 PDFs parsed successfully")

    # ---- AI Extraction ----
    inspection_data = extract_inspection(inspection_text, inspection_prompt)
    thermal_data = extract_thermal(thermal_text, thermal_prompt)

    print("🧠 Structured extraction complete")

    # ---- Merge Logic ----
    merged = merge_observations(inspection_data, thermal_data)

# NEW STEP — Confidence + Severity Scoring
    merged = compute_severity_and_confidence(merged)


    # Save structured data (VERY IMPORTANT for evaluation)
    with open("outputs/structured_data.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    print("🔗 Observations merged")

    # ---- Generate DDR ----
    final_report = generate_ddr(merged, ddr_prompt)

    with open("outputs/final_ddr.md", "w", encoding="utf-8") as f:
        f.write(final_report)

    print("📝 DDR report generated")

    # ---- Evaluator Guardrail ----
    evaluation = evaluate_ddr(merged, final_report)

    with open("outputs/evaluation.json", "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2)

    print("🛡️ Evaluation complete:", evaluation)

    # ---- Optional Safety Warning ----
    if evaluation.get("hallucination"):
        print("⚠️ WARNING: Possible hallucination detected.")

    print("✅ Pipeline Finished Successfully!")


# -------------------------
# Entry Point
# -------------------------
if __name__ == "__main__":
    run_pipeline()
