"""TruthLatch HTTP API."""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


# TRUTHLATCH_AUDIT_PATH lets tests and deployments choose the audit log location.
audit_log = AuditLog(os.environ.get("TRUTHLATCH_AUDIT_PATH", "data/audit.jsonl"))
registry = build_registry()

app = FastAPI(
    title="TruthLatch API",
    description="Evidence-based claim verification prototype.",
    version="0.1.0",
)

# Configure browser access explicitly for the frontend. Set
# TRUTHLATCH_CORS_ORIGINS to a comma-separated list of trusted frontend origins.
_default_cors_origins = "http://localhost:5173,http://127.0.0.1:5173"
allowed_origins = [
    origin.strip()
    for origin in os.environ.get(
        "TRUTHLATCH_CORS_ORIGINS", _default_cors_origins
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Accept", "Content-Type", "Authorization"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "truthlatch"}


@app.get("/api/v1/history", response_model=list[VerificationResponse])
def verification_history():
    """Return audit records with the newest decision first."""
    try:
        records = audit_log.get_history()
    except AuditError as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to load verification history",
        ) from exc

    return [record.model_dump(mode="json") for record in reversed(records)]


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
