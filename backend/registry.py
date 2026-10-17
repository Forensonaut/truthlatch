
"""In-memory registry for TruthLatch verification results."""

from threading import RLock

from pydantic import ValidationError

from backend.schemas import VerificationResponse


class RegistryError(Exception):
    """Base exception for registry operations."""


class DuplicateVerificationError(RegistryError):
    """Raised when a verification ID is already registered."""


class Registry:
    """Store and retrieve validated verification results."""

    def __init__(self):
        self._records: dict[str, VerificationResponse] = {}
        self._lock = RLock()

    @staticmethod
    def _validate_id(verification_id: str) -> str:
        """Validate and return a verification ID."""
        if not isinstance(verification_id, str):
            raise ValueError("verification_id must be a string")

        if not verification_id.strip():
            raise ValueError("verification_id must not be empty")

        return verification_id

    @staticmethod
    def _validate_result(result) -> VerificationResponse:
        """Convert a dictionary or model into a validated response."""
        try:
            validated = VerificationResponse.model_validate(result)
        except (ValidationError, TypeError, ValueError) as exc:
            raise ValueError(
                "Invalid verification result"
            ) from exc

        Registry._validate_id(validated.verification_id)
        return validated

    def register(self, result) -> VerificationResponse:
        """Register a result and return a copy of the stored record."""
        validated = self._validate_result(result)
        verification_id = validated.verification_id

        with self._lock:
            if verification_id in self._records:
                raise DuplicateVerificationError(
                    f"Verification already registered: {verification_id}"
                )

            self._records[verification_id] = validated.model_copy(deep=True)
            return self._records[verification_id].model_copy(deep=True)

    def lookup(
        self, verification_id: str
    ) -> VerificationResponse | None:
        """Return a copy of a record, or None if it doesn't exist."""
        verification_id = self._validate_id(verification_id)

        with self._lock:
            result = self._records.get(verification_id)

            if result is None:
                return None

            return result.model_copy(deep=True)

    def __len__(self) -> int:
        """Return the number of registered results."""
        with self._lock:
            return len(self._records)
