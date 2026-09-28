# CreativeOps Engine: AI Pipeline & Brand Governance Orchestrator

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Cloud-Ready](https://img.shields.io/badge/Architecture-Cloud--Native-green.svg)]()

> A production-grade creative transformation pipeline bridging enterprise marketing briefs with generative media execution (Veo 3.1, Seedance 2.5, Kling 3.0), enforcing programmatic brand governance and QA validation.

---

## The Business Problem

Enterprise creative teams face operational bottlenecks when scaling Generative AI:
1. **Prompt Inconsistency:** Fragmented prompts generate hallucinations, style drift, and broken anatomy.
2. **Lack of Governance:** No guardrails against brand guideline violations or forbidden keywords.
3. **Manual Overhead:** Hours wasted translating marketing briefs into camera-directed shot lists.

---

## Architecture

[ Marketing Brief ]
       │
       ▼
[ Pipeline Orchestrator ]
       │
       ▼
[ Shot Manifest Deconstruction ]
       │
       ▼
[ Technical Multimodal Prompts ]
       │
       ▼
[ Brand QA & Governance Engine ] ──(Fails Rules)──► [ Auto-Remediation ]
       │ (Compliant)
       ▼
[ Validated JSON Manifest ]
       │
       ▼
[ Cloud Endpoints (Veo / Seedance) ]

---

## Key Features

- **Automated Shot Deconstruction:** Breaks campaigns into timed sequential scenes (<= 8s limits) matching SOTA video model mechanics.
- **Deterministic QA & Brand Guardrails:** Programmatic verification of negative constraints, aspect ratios, focal lens specs, and forbidden vocabulary.
- **Multimodal Prompt Standards:** Structured 6-step formula (Subject, Action, Environment, Camera, Style, Constraints).
- **Containerized:** Docker packaging for immediate deployment on AWS ECS, GCP Cloud Run, or Kubernetes.

---

## Quickstart

### Local Execution

1. Install dependencies:
   pip install -r requirements.txt

2. Run the Streamlit application:
   streamlit run app.py

### Docker Execution

docker build -t creativeops-engine .
docker run -p 8501:8501 creativeops-engine

---

## Technical Stack

- **Core Engine:** Python 3.10+, Pydantic V2
- **Orchestration:** Custom Rule-Based Agent Pipeline
- **Interface:** Streamlit Web UI
- **Deployment:** Docker

---
**Author:** Charles Belfort — AI Creative Producer & Systems Engineer  
[LinkedIn Profile](https://www.linkedin.com/in/charlesbelfort)
