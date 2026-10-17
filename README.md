# CoreShift — TruthLatch

**Tagline:** Don't trust an AI's claim until the evidence agrees.

## Problem

AI agents can report that an action succeeded even when the underlying system state does not confirm the result. Relying on claims alone can lead to incomplete actions and unreliable audit records.

## Proposed solution

TruthLatch independently verifies AI execution claims against observed evidence and returns one of three outcomes:

- **VERIFIED** — sufficient evidence confirms the expected result.
- **CONTRADICTED** — evidence shows the claimed result was not achieved.
- **UNKNOWN** — evidence is missing, unavailable, stale, or inconclusive.

## Datathon

IBM Z Datathon 2026  
Team: CoreShift  
Theme: AI Secured — Innovation Without Exposure

## Development status

Project setup and planning.

Implementation will begin during the official datathon window.

## Planned technologies

- Python
- IBM LinuxONE Community Cloud
- AI/ML components
- Automated tests and evidence-linked audit records


## Run the local prototype

Requirements: Python 3.12 and Node.js 20 or later.

Start the API in one terminal:

```bash
python -m pip install -r requirements.txt
export TRUTHLATCH_REGISTRY=memory
export TRUTHLATCH_AUDIT_PATH=/tmp/truthlatch-audit.jsonl
export TRUTHLATCH_CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Start the frontend in another terminal from the repository root:

```bash
npm install
npm run dev
```

Open `http://localhost:5173`. The frontend uses the API at port 8000 on the same hostname. When running on a remote LinuxONE host, use SSH port forwarding for ports 5173 and 8000 rather than exposing these development servers publicly.

The local prototype uses an in-memory registry while Firebase credentials are not configured. The base `requirements.txt` intentionally omits Firebase's native gRPC dependencies so the UI/API prototype can run on IBM LinuxONE. For a supported environment where Firebase Admin's native dependencies install successfully, install `requirements-firebase.txt` to add Firestore support. Audit history is written to the path in `TRUTHLATCH_AUDIT_PATH`. This verifies the UI-to-API flow, not live Firestore connectivity. Never place Firebase service-account credentials in frontend files.
