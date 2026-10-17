# CoreShift — TruthLatch

**Tagline:** Don't trust an AI's claim until the evidence agrees.

TruthLatch independently checks an AI agent's claim about an action against observed evidence and returns one of three outcomes:

- **VERIFIED** — fresh, authoritative evidence supports the expected state.
- **CONTRADICTED** — fresh, authoritative evidence supports a declared contradictory state.
- **UNKNOWN** — evidence is missing, irrelevant, stale, non-authoritative, or conflicting.

## IBM Z Datathon 2026

- **Team:** CoreShift
- **Theme:** AI Secured — Innovation Without Exposure
- **Platform:** IBM LinuxONE Community Cloud

## Current prototype

The repository contains a FastAPI verification API, a React/Vite dashboard, a verification-history screen, and automated tests.

The currently demonstrated setup is a prototype: it uses an in-memory verification registry and a local JSON Lines audit log. The interface sends verification requests to the API and renders the returned decisions. **Live Firebase/Firestore connectivity has not been validated as part of the LinuxONE run-through.**

## Requirements

- Python 3.12
- Node.js 18 or later (Node.js 20+ is recommended; the CI build uses Node.js 20)
- npm
- Git

On Ubuntu/LinuxONE, install the system packages first:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nodejs npm pkg-config libssl-dev
```

Check your versions:

```bash
python3 --version
node --version
npm --version
```

## 1. Get the code and install dependencies

From the repository root:

```bash
git clone https://github.com/Forensonaut/truthlatch.git
cd truthlatch

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
npm install
```

If you already cloned the repository, use `cd /path/to/truthlatch` instead of cloning again, then update it with `git pull --ff-only origin main`.

## 2. Run the automated tests

Set the in-memory registry and audit-log path **before** running the tests. The test suite sends API requests, so leaving the registry on its default Firestore setting will make verification tests try to access Firebase.

```bash
cd /path/to/truthlatch
source .venv/bin/activate

export TRUTHLATCH_REGISTRY=memory
export TRUTHLATCH_AUDIT_PATH=/tmp/truthlatch-test-audit.jsonl
export TRUTHLATCH_CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"

python -m unittest discover -s tests -v
```

A successful run ends with `OK`. The test audit file is separate from the demo audit file used below.

## 3. Start TruthLatch locally

Run the **API** and **frontend** in separate terminals. Keep both running while using the app.

### Terminal A — API

From the repository root:

```bash
cd /path/to/truthlatch
source .venv/bin/activate

export TRUTHLATCH_REGISTRY=memory
export TRUTHLATCH_AUDIT_PATH=/tmp/truthlatch-audit.jsonl
export TRUTHLATCH_CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

The API listens locally on port `8000`. You can check its health at [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) from the same machine. FastAPI's interactive API docs are at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Terminal B — frontend

Open a second terminal, change to the repository root, and activate the virtual environment if you want to keep the same shell setup:

```bash
cd /path/to/truthlatch
npm run dev
```

Vite serves the UI at [http://localhost:5173](http://localhost:5173). The frontend calls the API at port `8000` on the same hostname. Keep both processes running.

### On a Mac or Linux laptop running everything locally

Use the same API and frontend commands above in two local terminal windows, then open [http://localhost:5173](http://localhost:5173) in your browser. No SSH tunnel is needed.

## 4. Run it on a remote IBM LinuxONE server

When the repository and both services run on LinuxONE, bind the development servers to `127.0.0.1` as shown above and use SSH port forwarding. **Do not expose the Vite or development API ports publicly.**

1. In a first SSH session, start the API using **Terminal A — API** above.
2. Open a second terminal on your laptop, SSH to the same server, and start the frontend using **Terminal B — frontend** above.
3. In a third terminal on your laptop (not inside either SSH session), forward both ports:

```bash
ssh -N -i ~/.ssh/YOUR_SSH_KEY \
  -L 5173:127.0.0.1:5173 \
  -L 8000:127.0.0.1:8000 \
  YOUR_USER@YOUR_LINUXONE_HOST
```

Replace `~/.ssh/YOUR_SSH_KEY`, `YOUR_USER`, and `YOUR_LINUXONE_HOST` with your key path, server username, and host. Leave the tunnel running, then open [http://localhost:5173](http://localhost:5173) on your laptop.

## 5. Try a verification

In the UI, choose **Run new verification** and use the following demo input:

- **Expected observation:** `user_access=revoked`
- **Evidence observations:** `user_access=revoked` (one observation per line)
- **Evidence source:** `demo-iam-registry`
- **Maximum evidence age:** `3600`
- **Mark supplied observations as authoritative:** checked for this demo only
- **Contradictory observations:** leave empty

Submit the form. The expected outcome is **VERIFIED** because the demo evidence matches the expected observation, is fresh, and is marked authoritative. Then open **Verification history** to see the recorded decision.

More useful cases:
- **CONTRADICTED:** expected `user_access=revoked`; evidence `user_access=active`; mark the evidence authoritative and add `user_access=active` under contradictory observations.
- **UNKNOWN:** provide no evidence, or leave evidence non-authoritative.

The form's authoritative checkbox is demonstration input, **not authentication of a real source**. Do not treat manually entered data as proof from an actual IAM or infrastructure system.

## Configuration and storage

- `TRUTHLATCH_REGISTRY=memory` selects an in-memory registry for the prototype. Registry data is not durable across backend restarts.
- `TRUTHLATCH_AUDIT_PATH` chooses the JSON Lines file used for the decision history. Keep the path consistent between runs if you want the history file to be reused.
- `TRUTHLATCH_CORS_ORIGINS` is a comma-separated allowlist of frontend origins. The default allows `http://localhost:5173` and `http://127.0.0.1:5173`.
- `VITE_API_BASE_URL` can override the API URL. If omitted, the frontend uses the page's hostname with port `8000`.

### Optional Firebase/Firestore mode

The base `requirements.txt` omits Firebase Admin's native gRPC dependencies so the in-memory prototype can be installed on IBM LinuxONE without building those dependencies there. In an environment that supports installing them, add Firebase support with:

```bash
pip install -r requirements-firebase.txt
```

Configure a Firebase service-account JSON key path through `FIREBASE_KEY_PATH` or place the key at `backend/serviceAccountKey.json` as expected by the backend. Keep service-account keys out of source control, frontend files, and logs. Rotate any credential that has been exposed.

Firestore mode is optional and is **not** covered by the demonstrated in-memory setup. Before using it, confirm that the Firebase project, access rules, credentials, and persistence behaviour work in the intended environment.

## Production note

The Vite server and Uvicorn command above are development settings, not a production deployment. For production, use a deployment-appropriate web server, TLS, authentication/authorization, restricted origins, durable storage, and authenticated evidence adapters. A manually checked authoritative flag is not a security boundary.

## Project layout

- `backend/` — FastAPI application, request/response schemas, registry, and audit logging
- `verification/` — deterministic evidence evaluation engine
- `frontend/` — React/Vite dashboard, new-verification form, outcome cards, and history table
- `tests/` — API, contract, audit, registry, timestamp, and verifier tests
- `schemas/` — verification contract/schema assets
