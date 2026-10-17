import unittest

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


class ApiTests(unittest.TestCase):
    def test_health(self):
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_verify_without_evidence_returns_unknown(self):
        response = client.post(
            "/api/v1/verify",
            json={
                "expected_observation": "user_access=revoked",
                "evidence": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "UNKNOWN")
        self.assertEqual(response.json()["evidence"], [])

    def test_invalid_request_is_rejected(self):
        response = client.post(
            "/api/v1/verify",
            json={"expected_observation": ""},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
