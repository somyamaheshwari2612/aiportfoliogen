"""
Unit tests for AI module (ai/gemini.py).
All tests use mocking — no real Gemini API calls are made.
"""

import json
import unittest
from unittest.mock import patch, MagicMock

from ai.gemini import generate_portfolio_json


class TestGeminiModule(unittest.TestCase):

    def test_empty_resume_text(self):
        """Passing empty text should raise ValueError before hitting the API."""
        # The prompt is still provided, but the resume_text is empty.
        # generate_portfolio_json sends both to Gemini; if Gemini returns
        # an empty response our code raises ValueError.
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_response = MagicMock()
                mock_response.text = ""
                mock_genai.Client.return_value.models.generate_content.return_value = mock_response

                with self.assertRaises(ValueError) as ctx:
                    generate_portfolio_json("", "system prompt")
                self.assertIn("empty response", str(ctx.exception).lower())

    def test_invalid_json_response(self):
        """If Gemini returns non-JSON text, we should get a clear error message."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_response = MagicMock()
                mock_response.text = "Sure! Here is your portfolio. Good luck!"
                mock_genai.Client.return_value.models.generate_content.return_value = mock_response

                with self.assertRaises(ValueError) as ctx:
                    generate_portfolio_json("John Doe\nEngineer", "system prompt")
                self.assertIn("incomplete JSON", str(ctx.exception))

    def test_truncated_json_response(self):
        """Simulates Gemini hitting max_output_tokens and cutting off mid-JSON."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_response = MagicMock()
                mock_response.text = '{"personal_info": {"name": "John Doe"}, "skills": ["Pyth'
                mock_genai.Client.return_value.models.generate_content.return_value = mock_response

                with self.assertRaises(ValueError) as ctx:
                    generate_portfolio_json("John Doe\nEngineer", "system prompt")
                self.assertIn("incomplete JSON", str(ctx.exception))

    def test_valid_json_response(self):
        """A well-formed JSON response should be returned as a Python dict."""
        valid_data = {
            "personal_info": {"name": "Jane Doe", "email": "jane@test.com"},
            "skills": ["Python", "Flask"],
            "experience": [],
            "education": [],
            "projects": []
        }
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_response = MagicMock()
                mock_response.text = json.dumps(valid_data)
                mock_genai.Client.return_value.models.generate_content.return_value = mock_response

                result = generate_portfolio_json("Jane Doe\nEngineer", "system prompt")
                self.assertIsInstance(result, dict)
                self.assertEqual(result["personal_info"]["name"], "Jane Doe")

    def test_is_resume_false_rejection(self):
        """If Gemini flags the file as not a resume, we should raise ValueError."""
        rejection_data = {
            "is_resume": False,
            "rejection_reason": "This appears to be a grocery list."
        }
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_response = MagicMock()
                mock_response.text = json.dumps(rejection_data)
                mock_genai.Client.return_value.models.generate_content.return_value = mock_response

                with self.assertRaises(ValueError) as ctx:
                    generate_portfolio_json("Buy milk, eggs, bread", "system prompt")
                self.assertIn("grocery list", str(ctx.exception))

    def test_missing_api_key(self):
        """Missing GEMINI_API_KEY should raise ValueError immediately."""
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                generate_portfolio_json("John Doe", "system prompt")
            self.assertIn("GEMINI_API_KEY", str(ctx.exception))

    def test_api_communication_failure(self):
        """If the Gemini API call itself throws, we should get a RuntimeError."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_genai.Client.return_value.models.generate_content.side_effect = \
                    Exception("Connection timed out")

                with self.assertRaises(RuntimeError) as ctx:
                    generate_portfolio_json("John Doe\nEngineer", "system prompt")
                self.assertIn("Failed to communicate", str(ctx.exception))

    def test_json_wrapped_in_markdown(self):
        """Gemini sometimes wraps JSON in markdown code fences — we should still parse it."""
        valid_data = {"personal_info": {"name": "Test"}, "skills": ["Python"]}
        markdown_response = f"```json\n{json.dumps(valid_data)}\n```"
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_response = MagicMock()
                mock_response.text = markdown_response
                mock_genai.Client.return_value.models.generate_content.return_value = mock_response

                result = generate_portfolio_json("Test User", "system prompt")
                self.assertIsInstance(result, dict)
                self.assertEqual(result["personal_info"]["name"], "Test")

    def test_none_response_object(self):
        """If the API returns None, we should get a clear error."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            with patch("ai.gemini.genai") as mock_genai:
                mock_genai.Client.return_value.models.generate_content.return_value = None

                with self.assertRaises(ValueError):
                    generate_portfolio_json("John Doe", "system prompt")


if __name__ == "__main__":
    unittest.main()
