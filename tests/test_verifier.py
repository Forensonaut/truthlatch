import unittest

from backend.schemas import VerificationRequest
from backend.verifier import verify_request


class VerifierAdapterTests(unittest.TestCase):
    def test_empty_evidence_returns_unknown(self):
        request = VerificationRequest(
            expected_observation="user_access=revoked",
            evidence=[],
        )

        result = verify_request(request)

        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["evidence"], [])
        self.assertTrue(result["verification_id"])
        self.assertTrue(result["checked_at"])


if __name__ == "__main__":
    unittest.main()
