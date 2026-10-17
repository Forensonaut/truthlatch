"""In-memory registry for tests and CI (no Firebase needed)."""

from threading import RLock

from backend.registry import DuplicateVerificationError, Registry
from backend.schemas import VerificationResponse


class InMemoryRegistry:
    def __init__(self):
        self._records: dict[str, VerificationResponse] = {}
        self._lock = RLock()

    def register(self, result) -> VerificationResponse:
        validated = Registry._validate_result(result)
        with self._lock:
            if validated.verification_id in self._records:
                raise DuplicateVerificationError(
                    f"Verification already registered: {validated.verification_id}"
                )
            self._records[validated.verification_id] = validated.model_copy(deep=True)
            return validated.model_copy(deep=True)

    def lookup(self, verification_id: str) -> VerificationResponse | None:
        verification_id = Registry._validate_id(verification_id)
        with self._lock:
            record = self._records.get(verification_id)
            return record.model_copy(deep=True) if record else None

    def __len__(self) -> int:
        with self._lock:
            return len(self._records)