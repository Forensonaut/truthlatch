"""In-memory fake Firestore client for testing."""

import copy
from typing import Any
from google.api_core.exceptions import AlreadyExists, ServiceUnavailable


class FakeSnapshot:
    """Fake document snapshot mimicking google.cloud.firestore DocumentSnapshot."""

    def __init__(self, exists: bool, data: dict[str, Any] | None = None):
        self.exists = exists
        self._data = copy.deepcopy(data) if data is not None else None

    def to_dict(self) -> dict[str, Any] | None:
        return copy.deepcopy(self._data)


class FakeAggregation:
    """Fake aggregation result holding a value."""

    def __init__(self, value: int):
        self.value = value


class FakeAggregationQuery:
    """Fake aggregation query mimicking collection.count()."""

    def __init__(self, collection: "FakeCollection"):
        self._collection = collection

    def get(self) -> list[list[FakeAggregation]]:
        self._collection._check_error()
        count = len(self._collection._docs)
        return [[FakeAggregation(count)]]


class FakeDocumentRef:
    """Fake document reference mimicking google.cloud.firestore DocumentReference."""

    def __init__(self, collection: "FakeCollection", doc_id: str):
        self._collection = collection
        self.id = doc_id
        self._error_to_raise: Exception | type[Exception] | None = None

    def set_error(self, error: Exception | type[Exception] | None):
        self._error_to_raise = error

    def _check_error(self):
        if self._error_to_raise:
            if isinstance(self._error_to_raise, type) and issubclass(self._error_to_raise, Exception):
                raise self._error_to_raise("Injected DocumentRef error")
            raise self._error_to_raise
        self._collection._check_error()

    def create(self, data: dict[str, Any]):
        self._check_error()
        if self.id in self._collection._docs:
            raise AlreadyExists(f"Document already exists: {self.id}")
        self._collection._docs[self.id] = copy.deepcopy(data)

    def get(self) -> FakeSnapshot:
        self._check_error()
        if self.id not in self._collection._docs:
            return FakeSnapshot(exists=False, data=None)
        return FakeSnapshot(exists=True, data=self._collection._docs[self.id])

    def delete(self):
        self._check_error()
        self._collection._docs.pop(self.id, None)


class FakeCollection:
    """Fake collection reference mimicking google.cloud.firestore CollectionReference."""

    def __init__(self, name: str):
        self.name = name
        self._docs: dict[str, dict[str, Any]] = {}
        self._error_to_raise: Exception | type[Exception] | None = None

    def set_error(self, error: Exception | type[Exception] | None):
        self._error_to_raise = error

    def _check_error(self):
        if self._error_to_raise:
            if isinstance(self._error_to_raise, type) and issubclass(self._error_to_raise, Exception):
                raise self._error_to_raise("Injected Collection error")
            raise self._error_to_raise

    def document(self, doc_id: str) -> FakeDocumentRef:
        return FakeDocumentRef(self, doc_id)

    def count(self) -> FakeAggregationQuery:
        return FakeAggregationQuery(self)


class FakeFirestore:
    """Fake Firestore client mimicking google.cloud.firestore.Client."""

    def __init__(self):
        self._collections: dict[str, FakeCollection] = {}

    def collection(self, name: str) -> FakeCollection:
        if name not in self._collections:
            self._collections[name] = FakeCollection(name)
        return self._collections[name]

    def set_error(
        self,
        error: Exception | type[Exception] | None,
        collection_name: str = "verifications",
    ):
        self.collection(collection_name).set_error(error)
