"""Additional API validation and verifier adapter tests."""
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.schemas import VerificationRequest
from backend.verifier import verify_request


client = TestClient(app)


class ApiEdgeTests(unittest.TestCase):
    def test_empty_expected_observation_is_rejected(self):
        response = client.post(
            "/api/v1/verify",
            json={"expected_observation": ""},
        )
        self.assertEqual(response.status_code, 422)

    def test_unexpected_request_field_is_rejected(self):
        response = client.post(
            "/api/v1/verify",
            json={
                "expected_observation": "user_access=revoked",
                "unexpected": True,
            },
        )
        self.assertEqual(response.status_code, 422)

    def test_evidence_missing_authoritative_is_rejected(self):
        response = client.post(
            "/api/v1/verify",
            json={
                "expected_observation": "user_access=revoked",
                "evidence": [{
                    "evidence_id": "e-1",
                    "source": "synthetic_iam",
                    "observation": "user_access=revoked",
                    "observed_at": "2026-10-17T10:00:00Z",
                }],
            },
        )
        self.assertEqual(response.status_code, 422)

    def test_evidence_with_unexpected_field_is_rejected(self):
        response = client.post(
            "/api/v1/verify",
            json={
                "expected_observation": "user_access=revoked",
                "evidence": [{
                    "evidence_id": "e-1",
                    "source": "synthetic_iam",
                    "observation": "user_access=revoked",
                    "observed_at": "2026-10-17T10:00:00Z",
                    "authoritative": True,
                    "extra_field": "unexpected",
                }],
            },
        )
        self.assertEqual(response.status_code, 422)


class VerifierAdapterEdgeTests(unittest.TestCase):
    @patch("backend.verifier.verify")
    def test_custom_max_age_is_forwarded(self, mocked_verify):
        mocked_verify.return_value = {"status": "UNKNOWN"}
        request = VerificationRequest(
            expected_observation="user_access=revoked",
            max_age_seconds=120,
        )

        verify_request(request)

        self.assertEqual(
            mocked_verify.call_args.kwargs["max_age_seconds"],
            120,
        )

    @patch("backend.verifier.verify")
    def test_contradictory_observations_are_forwarded(self, mocked_verify):
        mocked_verify.return_value = {"status": "UNKNOWN"}
        contradictions = ["user_access=active"]
        request = VerificationRequest(
            expected_observation="user_access=revoked",
            contradictory_observations=contradictions,
        )

        verify_request(request)

        self.assertEqual(
            mocked_verify.call_args.kwargs["contradictory_observations"],
            contradictions,
        )


if __name__ == "__main__":
    unittest.main()
