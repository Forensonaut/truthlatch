"""Firestore-backed registry for TruthLatch verification results."""

from google.api_core.exceptions import AlreadyExists, GoogleAPIError
from pydantic import ValidationError

from backend.firestore_client import get_db
from backend.schemas import VerificationResponse

COLLECTION = "verifications"


class RegistryError(Exception):
    """Base exception for registry operations."""


class DuplicateVerificationError(RegistryError):
    """Raised when a verification ID is already registered."""


class Registry:
    """Store and retrieve validated verification results in Firestore."""

    def __init__(self):
        # Connect lazily so importing the app never needs credentials.
        self._collection = None

    @property
    def _col(self):
        if self._collection is None:
            self._collection = get_db().collection(COLLECTION)
        return self._collection

    @staticmethod
    def _validate_id(verification_id: str) -> str:
        if not isinstance(verification_id, str):
            raise ValueError("verification_id must be a string")
        if not verification_id.strip():
            raise ValueError("verification_id must not be empty")
        if "/" in verification_id:
            raise ValueError("verification_id must not contain '/'")
        return verification_id

    @staticmethod
    def _validate_result(result) -> VerificationResponse:
        try:
            validated = VerificationResponse.model_validate(result)
        except (ValidationError, TypeError, ValueError) as exc:
            raise ValueError("Invalid verification result") from exc
        Registry._validate_id(validated.verification_id)
        return validated

    def register(self, result) -> VerificationResponse:
        validated = self._validate_result(result)
        try:
            self._col.document(validated.verification_id).create(
                validated.model_dump(mode="json")
            )
        except AlreadyExists as exc:
            raise DuplicateVerificationError(
                f"Verification already registered: {validated.verification_id}"
            ) from exc
        except GoogleAPIError as exc:
            raise RegistryError("Could not write to Firestore") from exc
        return validated.model_copy(deep=True)

    def lookup(self, verification_id: str) -> VerificationResponse | None:
        verification_id = self._validate_id(verification_id)
        try:
            snapshot = self._col.document(verification_id).get()
        except GoogleAPIError as exc:
            raise RegistryError("Could not read from Firestore") from exc
        if not snapshot.exists:
            return None
        return VerificationResponse.model_validate(snapshot.to_dict())

    def __len__(self) -> int:
        try:
            result = self._col.count().get()
            return int(result[0][0].value)
        except GoogleAPIError as exc:
            raise RegistryError("Could not count Firestore documents") from exc