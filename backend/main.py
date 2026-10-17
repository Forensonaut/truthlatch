"""TruthLatch HTTP API."""

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from backend.schemas import VerificationRequest, VerificationResponse
from backend.verifier import verify_request

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
        return VerificationResponse.model_validate(result)
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
