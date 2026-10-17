"""Integration tests for API verification statuses and the published schema."""

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

from backend.main import app


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts" / "verification.schema.json"

EXPECTED = "user_access=revoked"
CONTRADICTION = "user_access=active"

client = TestClient(app)


def utc_now():
    """Return a current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def evidence(observation, evidence_id):
    return {
        "evidence_id": evidence_id,
        "source": "synthetic_iam",
        "observation": observation,
        "observed_at": utc_now(),
        "authoritative": True,
    }


class ApiStatusContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open(encoding="utf-8") as schema_file:
            schema = json.load(schema_file)

        cls.validator = Draft202012Validator(schema)

    def verify(self, evidence_items):
        response = client.post(
            "/api/v1/verify",
            json={
                "expected_observation": EXPECTED,
                "evidence": evidence_items,
                "max_age_seconds": 3600,
                "contradictory_observations": [CONTRADICTION],
            },
        )

        self.assertEqual(
            response.status_code,
            200,
            msg=f"Unexpected response: {response.text}",
        )

        body = response.json()

        # Validate the actual HTTP response against the published contract.
        self.validator.validate(body)

        # Check the required top-level response fields.
        self.assertEqual(
            set(body),
            {
                "verification_id",
                "status",
                "explanation",
                "evidence",
                "checked_at",
            },
        )
        self.assertTrue(body["verification_id"])
        self.assertTrue(body["explanation"])
        self.assertTrue(body["checked_at"].endswith("Z"))

        return body

    def test_supporting_evidence_returns_schema_valid_verified(self):
        body = self.verify([evidence(EXPECTED, "e-verified")])

        self.assertEqual(body["status"], "VERIFIED")
        self.assertEqual(len(body["evidence"]), 1)
        self.assertEqual(
            body["evidence"][0]["observation"],
            EXPECTED,
        )

    def test_contradictory_evidence_returns_schema_valid_contradicted(self):
        body = self.verify([evidence(CONTRADICTION, "e-contradicted")])

        self.assertEqual(body["status"], "CONTRADICTED")
        self.assertEqual(len(body["evidence"]), 1)
        self.assertEqual(
            body["evidence"][0]["observation"],
            CONTRADICTION,
        )

    def test_conflicting_evidence_returns_schema_valid_unknown(self):
        body = self.verify([
            evidence(EXPECTED, "e-supporting"),
            evidence(CONTRADICTION, "e-contradicting"),
        ])

        self.assertEqual(body["status"], "UNKNOWN")
        self.assertIn("conflicts", body["explanation"])
        self.assertEqual(len(body["evidence"]), 2)

    def test_non_authoritative_evidence_cannot_verify_claim(self):
        item = evidence(EXPECTED, "e-untrusted")
        item["authoritative"] = False

        body = self.verify([item])

        self.assertEqual(body["status"], "UNKNOWN")
        self.assertEqual(body["evidence"], [])

    def test_irrelevant_evidence_is_excluded(self):
        item = evidence("unrelated_observation=value", "e-irrelevant")

        body = self.verify([item])

        self.assertEqual(body["status"], "UNKNOWN")
        self.assertEqual(body["evidence"], [])


if __name__ == "__main__":
    unittest.main()
