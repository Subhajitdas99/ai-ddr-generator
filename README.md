# 🧠 AI DDR Generator — Applied AI Builder Assignment

## 📌 Overview

This project implements a **fault-tolerant Applied AI workflow** that converts raw inspection and thermal documents into a structured **Detailed Diagnostic Report (DDR)**.

Instead of relying on a single LLM prompt, the system is designed as a **multi-stage AI pipeline** with deterministic reasoning layers, guardrails, and offline fallback execution to ensure reliability.

The goal is to demonstrate:

* Structured reasoning
* Reliable report generation
* Handling missing or conflicting data
* Reduced hallucinations through system design

---

## 🏗️ System Architecture

```
PDF Ingestion
      ↓
Structured Extraction (LLM + Offline Fallback)
      ↓
Merge + Conflict Reasoning Layer
      ↓
Confidence & Severity Scoring Engine
      ↓
Guardrailed DDR Generation (LLM + Offline Template)
      ↓
Evaluator Guardrail (Quality Check)
```

### Key Design Principle

> The LLM writes the report — but deterministic logic decides the facts.

---

## ⚙️ Features

### ✅ Structured Observation Extraction

* Parses inspection and thermal reports
* Produces JSON observations
* Uses offline rule-based fallback if API unavailable

### ✅ Logical Merge Engine

* Combines inspection + thermal findings
* Detects conflicts
* Avoids duplicate observations

### ✅ Confidence & Severity Scoring

Rule-based scoring adds:

* `severity_level`
* `confidence_score`
* `reasoning_note`

This ensures severity is not hallucinated by the model.

### ✅ Guardrailed DDR Generator

Strict rules enforced:

* No invented facts
* Missing info → `"Not Available"`
* Conflict reporting required
* Client-friendly language

### ✅ Offline Fallback Mode

If LLM APIs fail or quota is exceeded:

* Extraction switches to rule-based parser
* DDR generation switches to deterministic template
* Pipeline continues without crashing

### ✅ Evaluator Guardrail

Post-generation validation step that checks:

* Hallucinated content
* Missing-data violations
* Ignored conflicts

---

## 📂 Project Structure

```
ai-ddr-generator/
│
├── data/
├── outputs/
├── prompts/
└── src/
    ├── ingestion/
    ├── extraction/
    ├── reasoning/
    ├── generation/
    └── main.py
```

---

## 🚀 How to Run

From project root:

```
python -m src.main
```

Outputs will be saved in:

```
outputs/
 ├── final_ddr.md
 ├── structured_data.json
 └── evaluation.json
```

---

## 📄 Output Format (DDR Structure)

The generated report contains:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment (with reasoning)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

---

## 🛡️ Reliability Design Decisions

This project prioritizes **system thinking over prompting**:

* Extraction, reasoning, and generation are separated.
* Severity scoring is deterministic.
* Offline execution path prevents pipeline failure.
* Evaluator guardrail validates final output.

---

## ⚠️ Limitations

* Offline fallback uses simple keyword heuristics.
* Domain-specific ontology could improve root-cause reasoning.
* Thermal image data is treated as text input (no CV analysis).

---

## 🔧 Future Improvements

* Retrieval-Augmented Generation (RAG) grounding
* Domain knowledge graph for defect reasoning
* Confidence calibration using historical inspection data
* Advanced conflict-resolution logic
* Evaluation metrics dashboard

---

## 🎥 Loom Walkthrough

The Loom video explains:

* What was built
* Architecture and workflow
* Reliability strategies
* Known limitations and future improvements

---

## 👨‍💻 Author

Applied AI Builder Assignment Submission
Designed with a focus on **robust AI system architecture** rather than UI complexity.
