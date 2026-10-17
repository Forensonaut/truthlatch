"""Regression tests for TruthLatch API error handling."""

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app, raise_server_exceptions=False)


class ApiErrorHandlingTests(unittest.TestCase):
    @patch("backend.main.verify_request")
    def test_unexpected_internal_error_returns_generic_500(self, mocked_verify):
        mocked_verify.side_effect = RuntimeError("internal secret detail")

        response = client.post(
            "/api/v1/verify",
            json={"expected_observation": "user_access=revoked"},
        )

        self.assertEqual(response.status_code, 500)
        self.assertNotIn("internal secret detail", response.text)

    @patch("backend.main.verify_request")
    def test_invalid_internal_result_is_not_reported_as_client_error(
        self, mocked_verify
    ):
        mocked_verify.return_value = {"status": "NOT_A_VALID_STATUS"}

        response = client.post(
            "/api/v1/verify",
            json={"expected_observation": "user_access=revoked"},
        )

        self.assertEqual(
            response.status_code,
            500,
            msg=f"Unexpected response: {response.text}",
        )
        self.assertNotIn("NOT_A_VALID_STATUS", response.text)


if __name__ == "__main__":
    unittest.main()
