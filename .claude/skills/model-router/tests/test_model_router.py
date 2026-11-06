#!/usr/bin/env python3
"""Unit tests for Model Router & Failover Engine."""

import io
import json
import os
import sys
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

# Add parent scripts directory to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from router import ModelRouter, run_mcp_server


class TestModelRouter(unittest.TestCase):
    def setUp(self):
        self.router = ModelRouter(config_path="/tmp/nonexistent_config.json")

    def test_provider_status_structure(self):
        status = self.router.get_provider_status()
        self.assertIn("deepseek", status)
        self.assertIn("qwen", status)
        self.assertIn("groq", status)
        self.assertIn("openrouter", status)
        self.assertFalse(status["deepseek"]["ready"])

    def test_ranked_models_order(self):
        models = self.router.get_ranked_models()
        self.assertGreaterEqual(len(models), 10)
        # Verify best models are at the top and legacy at the bottom
        top_model = models[0]
        bottom_model = models[-1]
        self.assertIn("Tier 1", top_model["tier"])
        self.assertIn("Tier 4", bottom_model["tier"])
        self.assertGreater(top_model["score"], bottom_model["score"])

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "sk-fake-deepseek"})
    def test_env_key_injection(self):
        router = ModelRouter(config_path="/tmp/nonexistent_config.json")
        status = router.get_provider_status()
        self.assertTrue(status["deepseek"]["ready"])
        self.assertIn("api_key", router.config["providers"]["deepseek"])

    @patch("urllib.request.urlopen")
    def test_query_success(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps({
            "choices": [{"message": {"content": "Hello from DeepSeek", "reasoning": "Step 1"}}],
            "usage": {"total_tokens": 42},
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        # Inject key
        self.router.config["providers"]["deepseek"] = {"api_key": "sk-fake"}
        res = self.router.query("deepseek", "deepseek-reasoner", [{"role": "user", "content": "Hi"}])
        self.assertTrue(res["success"])
        self.assertEqual(res["content"], "Hello from DeepSeek")
        self.assertEqual(res["reasoning"], "Step 1")

    @patch("urllib.request.urlopen")
    def test_cascade_failover_on_429(self, mock_urlopen):
        """Tests that when primary provider hits 429, router cascades to fallback."""
        err_429 = urllib.error.HTTPError(
            url="https://api.deepseek.com",
            code=429,
            msg="Too Many Requests",
            hdrs={},
            fp=io.BytesIO(b'{"error": "Rate limit exceeded"}')
        )
        
        mock_success = MagicMock()
        mock_success.status = 200
        mock_success.read.return_value = json.dumps({
            "choices": [{"message": {"content": "Fallback answer from OpenRouter"}}],
            "usage": {"total_tokens": 55},
        }).encode("utf-8")
        mock_success.__enter__.return_value = mock_success

        mock_urlopen.side_effect = [err_429, mock_success]

        self.router.config["providers"]["deepseek"] = {"api_key": "sk-deepseek"}
        self.router.config["providers"]["openrouter"] = {"api_key": "sk-openrouter"}

        res = self.router.cascade_query("reason", [{"role": "user", "content": "Complex query"}])
        self.assertTrue(res["success"])
        self.assertEqual(res["provider"], "openrouter")
        self.assertEqual(res["content"], "Fallback answer from OpenRouter")
        self.assertEqual(len(res["attempts"]), 1)
        self.assertEqual(res["attempts"][0]["http_status"], 429)

    def test_mcp_server_protocol(self):
        """Tests MCP JSON-RPC initialization and tool discovery."""
        input_lines = (
            json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}) + "\n"
            + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n"
        )
        fake_stdin = io.StringIO(input_lines)
        fake_stdout = io.StringIO()

        with patch("sys.stdin", fake_stdin), patch("sys.stdout", fake_stdout):
            run_mcp_server(self.router)

        output_lines = [json.loads(line) for line in fake_stdout.getvalue().strip().split("\n") if line]
        self.assertEqual(len(output_lines), 2)
        self.assertEqual(output_lines[0]["result"]["serverInfo"]["name"], "model-router")
        tool_names = [t["name"] for t in output_lines[1]["result"]["tools"]]
        self.assertIn("consult_model", tool_names)
        self.assertIn("cascade_query", tool_names)
        self.assertIn("list_ranked_models", tool_names)
        self.assertIn("list_providers", tool_names)


if __name__ == "__main__":
    unittest.main()
