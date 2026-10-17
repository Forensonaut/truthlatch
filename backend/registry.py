"""Firestore-backed registry for TruthLatch verification results."""

from google.api_core.exceptions import AlreadyExists, GoogleAPIError
from pydantic import ValidationError

from backend.firestore_client import get_db
from backend.schemas import VerificationResponse


class RegistryError(Exception):
    """Base exception for registry operations."""


class DuplicateVerificationError(RegistryError):
    """Raised when a verification ID is already registered."""


class Registry:
    """Store and retrieve validated verification results in Firestore."""

    def __init__(self):
        self._db = get_db()
        self._collection = self._db.collection("verifications")

    @staticmethod
    def _validate_id(verification_id: str) -> str:
        """Validate and return a verification ID."""
        if not isinstance(verification_id, str):
            raise ValueError("verification_id must be a string")

        if not verification_id.strip():
            raise ValueError("verification_id must not be empty")

        if "/" in verification_id:
            raise ValueError("verification_id must not contain '/'")

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
        doc_ref = self._collection.document(verification_id)
        data = validated.model_dump(mode="json")

        try:
            doc_ref.create(data)
        except AlreadyExists as exc:
            raise DuplicateVerificationError(
                f"Verification already registered: {verification_id}"
            ) from exc
        except GoogleAPIError as exc:
            raise RegistryError(
                f"Failed to register verification {verification_id}: {exc}"
            ) from exc

        return validated.model_copy(deep=True)

    def lookup(
        self, verification_id: str
    ) -> VerificationResponse | None:
        """Return a copy of a record, or None if it doesn't exist."""
        verification_id = self._validate_id(verification_id)
        doc_ref = self._collection.document(verification_id)

        try:
            snapshot = doc_ref.get()
        except GoogleAPIError as exc:
            raise RegistryError(
                f"Failed to lookup verification {verification_id}: {exc}"
            ) from exc

        if not snapshot.exists:
            return None

        return VerificationResponse.model_validate(snapshot.to_dict())

    def __len__(self) -> int:
        """Return the number of registered results."""
        try:
            results = self._collection.count().get()
            return int(results[0][0].value)
        except GoogleAPIError as exc:
            raise RegistryError(
                f"Failed to count verifications: {exc}"
            ) from exc
