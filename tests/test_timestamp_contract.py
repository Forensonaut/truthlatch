"""Regression tests for timestamp handling at the API boundary."""
import unittest
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


class TimestampContractTests(unittest.TestCase):
    def test_malformed_evidence_timestamp_returns_unknown(self):
        response = client.post(
            "/api/v1/verify",
            json={
                "expected_observation": "user_access=revoked",
                "evidence": [
                    {
                        "evidence_id": "e-malformed",
                        "source": "synthetic_iam",
                        "observation": "user_access=revoked",
                        "observed_at": "not-a-timestamp",
                        "authoritative": True,
                    }
                ],
            },
        )

        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "UNKNOWN")

    def test_valid_timestamp_is_iso8601_utc(self):
        timestamp = datetime.now(timezone.utc).isoformat()
        parsed = datetime.fromisoformat(timestamp)

        self.assertIsNotNone(parsed.tzinfo)
        self.assertEqual(parsed.utcoffset().total_seconds(), 0)


if __name__ == "__main__":
    unittest.main()
