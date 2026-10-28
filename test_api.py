"""
Integration tests for FastAPI REST endpoints.
"""

import unittest
from starlette.testclient import TestClient
from promptguard.api.server import app

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["service"], "PromptGuard API")
        self.assertEqual(data["status"], "online")

    def test_list_scenarios(self):
        response = self.client.get("/api/scenarios")
        self.assertEqual(response.status_code, 200)
        scenarios = response.json()
        self.assertGreater(len(scenarios), 0)
        self.assertTrue(any(s["id"] == "scen-banking" for s in scenarios))

    def test_list_attacks(self):
        response = self.client.get("/api/attacks")
        self.assertEqual(response.status_code, 200)
        attacks = response.json()
        self.assertGreater(len(attacks), 10)

    def test_list_presets(self):
        response = self.client.get("/api/defenses/presets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("presets", data)

    def test_single_test_endpoint(self):
        payload = {
            "scenario_id": "scen-banking",
            "attack_id": "dir-01",
            "defense_preset": "none",
            "model_provider": "simulator"
        }
        response = self.client.post("/api/test", json=payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["is_vulnerable"])
        self.assertEqual(result["status"], "INJECTION_SUCCESSFUL")

if __name__ == "__main__":
    unittest.main()
