
"""Persistent audit log for TruthLatch verification decisions."""

import json
from pathlib import Path
from threading import RLock

from pydantic import ValidationError

from backend.schemas import VerificationResponse


class AuditError(Exception):
    """Base exception for audit-log failures."""


class AuditLog:
    """Append and retrieve validated verification decisions."""

    def __init__(self, path="data/audit.jsonl"):
        self._path = Path(path)
        self._lock = RLock()

    @staticmethod
    def _validate_result(result):
        """Validate a dictionary or VerificationResponse."""
        try:
            return VerificationResponse.model_validate(result)
        except (ValidationError, TypeError, ValueError) as exc:
            raise ValueError("Invalid verification result") from exc

    def record_decision(self, result):
        """Persist one completed verification decision."""
        validated = self._validate_result(result)
        line = json.dumps(validated.model_dump(mode="json"))

        try:
            with self._lock:
                self._path.parent.mkdir(parents=True, exist_ok=True)
                with self._path.open("a", encoding="utf-8") as file:
                    file.write(line + "\n")
        except OSError as exc:
            raise AuditError("Could not persist audit decision") from exc

        return validated.model_copy(deep=True)

    def get_history(self):
        """Return all valid decisions in insertion order."""
        if not self._path.exists():
            return []

        records = []

        try:
            with self._lock:
                with self._path.open("r", encoding="utf-8") as file:
                    for line_number, line in enumerate(file, start=1):
                        if not line.strip():
                            continue

                        try:
                            data = json.loads(line)
                            record = VerificationResponse.model_validate(data)
                        except (json.JSONDecodeError, ValidationError) as exc:
                            raise AuditError(
                                f"Invalid audit record on line {line_number}"
                            ) from exc

                        records.append(record)
        except OSError as exc:
            raise AuditError("Could not read audit history") from exc

        return records
