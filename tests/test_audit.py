
"""Tests for the TruthLatch audit log."""

import tempfile
import unittest
from pathlib import Path

from backend.audit import AuditLog, AuditError


def make_result(verification_id="verification-001", status="VERIFIED"):
    return {
        "verification_id": verification_id,
        "status": status,
        "explanation": "Fresh authoritative evidence supports the outcome.",
        "evidence": [],
        "checked_at": "2026-10-17T14:30:00Z",
    }


class TestAuditLog(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "audit.jsonl"
        self.audit = AuditLog(self.log_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_record_and_retrieve_decision(self):
        result = make_result()

        self.audit.record_decision(result)
        history = self.audit.get_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].verification_id, "verification-001")
        self.assertEqual(history[0].status, "VERIFIED")

    def test_missing_log_returns_empty_history(self):
        self.assertEqual(self.audit.get_history(), [])

    def test_history_survives_new_instance(self):
        self.audit.record_decision(make_result())

        another_audit = AuditLog(self.log_path)

        self.assertEqual(len(another_audit.get_history()), 1)

    def test_multiple_decisions_preserve_order(self):
        self.audit.record_decision(make_result("id-1", "VERIFIED"))
        self.audit.record_decision(make_result("id-2", "UNKNOWN"))
        self.audit.record_decision(make_result("id-3", "CONTRADICTED"))

        history = self.audit.get_history()

        self.assertEqual(
            [item.verification_id for item in history],
            ["id-1", "id-2", "id-3"],
        )

    def test_invalid_result_is_rejected(self):
        invalid = make_result()
        invalid.pop("status")

        with self.assertRaises(ValueError):
            self.audit.record_decision(invalid)

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            self.audit.record_decision(make_result(status="MAYBE"))

    def test_corrupted_log_is_reported(self):
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text("not valid JSON\n", encoding="utf-8")

        with self.assertRaises(AuditError):
            self.audit.get_history()


if __name__ == "__main__":
    unittest.main()
