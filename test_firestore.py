"""Test script to verify Firestore-backed Registry operations."""

from uuid import uuid4
from backend.registry import Registry, DuplicateVerificationError
from backend.schemas import VerificationResponse


def main():
    registry = Registry()
    test_id = f"test-{uuid4()}"
    record = VerificationResponse(
        verification_id=test_id,
        status="UNKNOWN",
        explanation="test",
        evidence=[],
        checked_at="2026-10-17T12:00:00Z",
    )

    try:
        # 1. Register test record
        reg_result = registry.register(record)
        print("Register result:", reg_result)

        # 2. Lookup registered ID
        lookup_result = registry.lookup(test_id)
        print("Lookup registered ID:", lookup_result)

        # 3. Lookup nonexistent ID (expect None)
        nonexistent_id = f"nonexistent-{uuid4()}"
        lookup_none = registry.lookup(nonexistent_id)
        print("Lookup nonexistent ID (expected None):", lookup_none)

        # 4. Attempt duplicate registration (expect DuplicateVerificationError)
        try:
            registry.register(record)
            print("FAILED: Expected DuplicateVerificationError was not raised")
        except DuplicateVerificationError as exc:
            print("Duplicate register caught expected exception:", type(exc).__name__, exc)

        # 5. len(registry)
        length = len(registry)
        print("Registry length:", length)

    finally:
        # Clean up test document
        print(f"Cleaning up test document {test_id}...")
        registry._collection.document(test_id).delete()
        print("Cleaned up successfully.")


if __name__ == "__main__":
    main()
