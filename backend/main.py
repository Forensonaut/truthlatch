"""TruthLatch HTTP API."""

import os

from fastapi import FastAPI, HTTPException
from backend.audit import AuditLog, AuditError
from backend.memory_registry import InMemoryRegistry
from backend.registry import Registry, RegistryError
from backend.schemas import VerificationRequest, VerificationResponse
from backend.verifier import verify_request


def build_registry():
    """Firestore by default; in-memory when TRUTHLATCH_REGISTRY=memory."""
    if os.environ.get("TRUTHLATCH_REGISTRY", "firestore").lower() == "memory":
        return InMemoryRegistry()
    return Registry()


# TRUTHLATCH_AUDIT_PATH lets tests write the audit log to a throwaway file.
audit_log = AuditLog(os.environ.get("TRUTHLATCH_AUDIT_PATH", "data/audit.jsonl"))
registry = build_registry()

app = FastAPI(
    title="TruthLatch API",
    description="Evidence-based claim verification prototype.",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "truthlatch"}


@app.post("/api/v1/verify", response_model=VerificationResponse)
def verify_endpoint(request: VerificationRequest):
    try:
        result = verify_request(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    # Validate the result produced by the verification engine.
    response = VerificationResponse.model_validate(result)

    # Store the verification result in the registry.
    try:
        registry.register(response)
    except (ValueError, RegistryError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to store verification result",
        ) from exc

    # Record the decision in the audit log.
    try:
        audit_log.record_decision(response)
    except AuditError as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to record verification audit",
        ) from exc

    return response