import unittest

from verification.engine import verify


NOW = "2026-10-17T12:00:00Z"
EXPECTED = "user_access=revoked"
CONTRADICTIONS = ["user_access=active"]


def item(observation, evidence_id="e-1", authoritative=True,
         observed_at="2026-10-17T11:55:00Z"):
    return {
        "evidence_id": evidence_id,
        "source": "synthetic_iam",
        "observation": observation,
        "observed_at": observed_at,
        "authoritative": authoritative,
    }


class VerificationEngineTests(unittest.TestCase):
    def run_check(self, evidence):
        return verify(
            EXPECTED,
            evidence,
            checked_at=NOW,
            max_age_seconds=3600,
            contradictory_observations=CONTRADICTIONS,
        )

    def test_verified(self):
        self.assertEqual(
            self.run_check([item(EXPECTED)])["status"], "VERIFIED"
        )

    def test_contradicted(self):
        self.assertEqual(
            self.run_check([item("user_access=active")])["status"],
            "CONTRADICTED",
        )

    def test_missing_evidence(self):
        self.assertEqual(self.run_check([])["status"], "UNKNOWN")

    def test_stale_evidence(self):
        old = item(EXPECTED, observed_at="2026-10-17T10:00:00Z")
        self.assertEqual(self.run_check([old])["status"], "UNKNOWN")

    def test_conflicting_evidence(self):
        evidence = [
            item(EXPECTED, "e-1"),
            item("user_access=active", "e-2"),
        ]
        self.assertEqual(self.run_check(evidence)["status"], "UNKNOWN")

    def test_non_authoritative_evidence(self):
        self.assertEqual(
            self.run_check([item(EXPECTED, authoritative=False)])["status"],
            "UNKNOWN",
        )


if __name__ == "__main__":
    unittest.main()
