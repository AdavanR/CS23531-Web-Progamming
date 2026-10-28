# 🛡️ PromptGuard Red-Teaming Security Audit Report
**Target System:** FinSecure Banking Assistant
**Audit Timestamp:** 2026-10-29 00:28:26
**Evaluator Engine:** promptguard-engine-v1 (Simulator)
**OWASP LLM Category:** LLM01:2025 - Prompt Injection

---
## 1. Executive Summary
PromptGuard completed an automated adversarial red-teaming evaluation of **FinSecure Banking Assistant**. A total of **88 attack iterations** were conducted across multiple defense postures. Under unprotected baseline conditions, the system exhibited an **Attack Success Rate (ASR) of 100.0%**, confirming critical vulnerability to Direct Instruction Overrides, Jailbreaks, and Secret Extraction.

- **Overall Attack Success Rate (All Presets):** `25.0%`
- **Proactive Defense Block Rate:** `35.23%`
- **False Positive Rate (Benign Control):** `10.0%`
- **Average Evaluation Latency:** `0.15 ms`

## 2. Defense Preset Comparison
| Defense Preset | Total Attacks | Succeeded (ASR) | Blocked (DBR) | Avg Latency |
|---|---|---|---|---|
| **No Defense (Vulnerable Baseline)** | 22 | `100.0%` | `0.0%` | 0.23 ms |
| **Baseline Heuristics** | 22 | `0.0%` | `50.0%` | 0.23 ms |
| **Structural Delimiters & Canary** | 22 | `0.0%` | `0.0%` | 0.06 ms |
| **Full Multi-Layer Guardrails** | 22 | `0.0%` | `90.91%` | 0.08 ms |


## 3. Vulnerability Breakdown by Category
| Attack Category | Total Tests | Compromised | Blocked | Neutralized | Category ASR |
|---|---|---|---|---|---|
| Direct Injection | 20 | 5 | 9 | 6 | **25.0%** |
| Indirect Injection | 12 | 3 | 4 | 5 | **25.0%** |
| Obfuscation & Encoding | 16 | 4 | 8 | 4 | **25.0%** |
| Jailbreak / Roleplay | 12 | 3 | 4 | 5 | **25.0%** |
| System Prompt Extraction | 12 | 3 | 3 | 6 | **25.0%** |
| Data Exfiltration | 8 | 2 | 2 | 4 | **25.0%** |
| Context & Multi-Turn Manipulation | 8 | 2 | 1 | 5 | **25.0%** |


## 4. Key Security Findings & Observations
1. **Vulnerability to Direct Instruction Overrides:** Without structural delimiters, naive LLM concatenation allows user input to overpower system instructions.
2. **System Prompt & Secret Canary Leakage:** Attackers can extract confidential system variables using verbatim extraction requests or JSON translation bypasses.
3. **Efficacy of Structural Delimiters:** Implementing `<user_untrusted_input>` boundary tags coupled with post-prompt instruction reinforcement reduced the Attack Success Rate to **0.0%**.
4. **False Positive Management:** The multi-layer guardrail achieved high protection while maintaining a low False Positive Rate on benign user inquiries.

## 5. Mitigation Roadmap & Best Practices
- **Adopt Strict Delimited Context Framing:** Always encapsulate untrusted user input within distinct tags (`<user_untrusted_input>`) and instruct the LLM to treat content within tags strictly as untrusted data.
- **Deploy Dual-LLM Guard / Intent Inspection:** Utilize a lightweight intent classifier to intercept adversarial payloads before they reach primary application models.
- **Canary Token Verification:** Embed randomized canary tokens in system contexts and scan output streams for unauthorized leakage.
- **Output Sanitization:** Strip markdown image tags (`![exfil](...)`) pointing to unverified external domains to prevent asynchronous exfiltration.
