"""Validate real API responses against the published JSON Schema."""
import json
import unittest
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from backend.main import app


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts" / "verification.schema.json"

client = TestClient(app)


class ApiResponseContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open(encoding="utf-8") as file:
            schema = json.load(file)

        cls.validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )

    def test_unknown_api_response_matches_published_schema(self):
        response = client.post(
            "/api/v1/verify",
            json={
                "expected_observation": "user_access=revoked",
                "evidence": [],
            },
        )

        self.assertEqual(response.status_code, 200, response.text)

        payload = response.json()
        errors = list(self.validator.iter_errors(payload))

        self.assertEqual(
            errors,
            [],
            "\n".join(error.message for error in errors),
        )

    def test_api_response_has_valid_utc_checked_at(self):
        response = client.post(
            "/api/v1/verify",
            json={"expected_observation": "user_access=revoked"},
        )

        self.assertEqual(response.status_code, 200, response.text)

        checked_at = response.json()["checked_at"]
        parsed = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))

        self.assertIsNotNone(parsed.tzinfo)
        self.assertEqual(parsed.utcoffset().total_seconds(), 0)

    def test_api_response_uses_only_permitted_statuses(self):
        response = client.post(
            "/api/v1/verify",
            json={"expected_observation": "user_access=revoked"},
        )

        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn(
            response.json()["status"],
            {"VERIFIED", "CONTRADICTED", "UNKNOWN"},
        )


if __name__ == "__main__":
    unittest.main()
