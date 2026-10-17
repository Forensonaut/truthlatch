"""TruthLatch HTTP API."""

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from backend.registry import Registry, RegistryError
from backend.schemas import VerificationRequest, VerificationResponse
from backend.verifier import verify_request
from backend.audit import AuditLog, AuditError

audit_log = AuditLog()
registry = Registry()

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


    