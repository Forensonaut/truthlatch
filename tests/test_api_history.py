"""Tests for the API's audit-backed verification history endpoint."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.audit import AuditLog
from backend.main import app


class ApiHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.audit_log = AuditLog(Path(self.temp_dir.name) / "audit.jsonl")
        audit_patcher = patch("backend.main.audit_log", self.audit_log)
        audit_patcher.start()
        self.addCleanup(audit_patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)
        self.client = TestClient(app)

    def test_history_returns_empty_list_when_no_decisions_exist(self):
        response = self.client.get("/api/v1/history")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_history_returns_recorded_decisions_newest_first(self):
        self.audit_log.record_decision({
            "verification_id": "history-old",
            "status": "UNKNOWN",
            "explanation": "No sufficient fresh authoritative evidence was found.",
            "evidence": [],
            "checked_at": "2026-10-17T10:00:00Z",
        })
        self.audit_log.record_decision({
            "verification_id": "history-new",
            "status": "VERIFIED",
            "explanation": "Fresh authoritative evidence supports the expected state.",
            "evidence": [],
            "checked_at": "2026-10-17T11:00:00Z",
        })

        response = self.client.get("/api/v1/history")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [record["verification_id"] for record in response.json()],
            ["history-new", "history-old"],
        )


if __name__ == "__main__":
    unittest.main()
