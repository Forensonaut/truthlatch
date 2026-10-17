"""Registry tests will be added when the registry interface is agreed."""

"""Tests for the TruthLatch verification registry."""

import unittest

from backend.registry import (
    Registry,
    DuplicateVerificationError,
)
from backend.schemas import VerificationResponse


def make_result(
    verification_id="verification-001",
    status="VERIFIED",
):
    return {
        "verification_id": verification_id,
        "status": status,
        "explanation": "Evidence supports the expected state.",
        "evidence": [],
        "checked_at": "2026-10-17T14:30:00Z",
    }


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()

    def test_register_and_lookup(self):
        result = make_result()

        stored = self.registry.register(result)

        self.assertIsInstance(stored, VerificationResponse)
        self.assertEqual(stored.verification_id, "verification-001")
        self.assertEqual(self.registry.lookup("verification-001"), stored)

    def test_missing_entry_returns_none(self):
        self.assertIsNone(self.registry.lookup("does-not-exist"))

    def test_empty_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.registry.lookup(" ")

    def test_non_string_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.registry.lookup(None)

    def test_invalid_result_is_rejected(self):
        invalid = make_result()
        del invalid["status"]

        with self.assertRaises(ValueError):
            self.registry.register(invalid)

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            self.registry.register(make_result(status="MAYBE"))

    def test_empty_verification_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.registry.register(make_result(verification_id=" "))

    def test_duplicate_id_is_rejected(self):
        self.registry.register(make_result())

        with self.assertRaises(DuplicateVerificationError):
            self.registry.register(
                make_result(status="CONTRADICTED")
            )

        # The original record must remain unchanged.
        self.assertEqual(
            self.registry.lookup("verification-001").status,
            "VERIFIED",
        )

    def test_returned_record_cannot_mutate_storage(self):
        self.registry.register(make_result())

        retrieved = self.registry.lookup("verification-001")
        retrieved.explanation = "Modified externally"

        self.assertEqual(
            self.registry.lookup("verification-001").explanation,
            "Evidence supports the expected state.",
        )

    def test_length(self):
        self.assertEqual(len(self.registry), 0)

        self.registry.register(make_result())

        self.assertEqual(len(self.registry), 1)


if __name__ == "__main__":
    unittest.main()
