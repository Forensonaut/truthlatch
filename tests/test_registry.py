"""Tests for the TruthLatch verification registry."""

import unittest
from unittest.mock import patch
from google.api_core.exceptions import ServiceUnavailable

from backend.registry import (
    Registry,
    RegistryError,
    DuplicateVerificationError,
)
from backend.schemas import VerificationResponse
from tests.fake_firestore import FakeFirestore


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
        self.fake_db = FakeFirestore()
        patcher = patch("backend.registry.get_db", return_value=self.fake_db)
        patcher.start()
        self.addCleanup(patcher.stop)
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

    def test_write_failure_raises_registry_error(self):
        self.fake_db.set_error(ServiceUnavailable("Firestore write error"))
        with self.assertRaises(RegistryError) as ctx:
            self.registry.register(make_result(verification_id="test-write-fail"))
        self.assertNotIsInstance(ctx.exception, DuplicateVerificationError)

    def test_read_failure_raises_registry_error(self):
        self.registry.register(make_result(verification_id="test-read-fail"))
        self.fake_db.set_error(ServiceUnavailable("Firestore read error"))
        with self.assertRaises(RegistryError):
            self.registry.lookup("test-read-fail")

    def test_slash_in_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.registry.lookup("invalid/id")

        with self.assertRaises(ValueError):
            self.registry.register(make_result(verification_id="invalid/id"))

    def test_record_round_trips_with_evidence(self):
        evidence_item = {
            "evidence_id": "ev-123",
            "source": "auth-service",
            "observation": "user_access=revoked",
            "observed_at": "2026-10-17T14:29:59Z",
            "authoritative": True,
        }
        result = {
            "verification_id": "v-roundtrip-001",
            "status": "VERIFIED",
            "explanation": "Verified with evidence item.",
            "evidence": [evidence_item],
            "checked_at": "2026-10-17T14:30:00Z",
        }
        stored = self.registry.register(result)
        retrieved = self.registry.lookup("v-roundtrip-001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved, stored)
        self.assertEqual(len(retrieved.evidence), 1)
        self.assertEqual(retrieved.evidence[0].evidence_id, "ev-123")
        self.assertEqual(retrieved.evidence[0].authoritative, True)


if __name__ == "__main__":
    unittest.main()
