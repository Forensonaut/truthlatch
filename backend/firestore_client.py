"""Firestore client initialization and provider for TruthLatch backend.

Firebase dependencies are imported lazily so the in-memory prototype can run on
LinuxONE without building native Firestore/gRPC dependencies.
"""

import os
from pathlib import Path
from typing import Any


def get_db() -> Any:
    """Return a Firestore client, initializing Firebase when optional deps exist."""
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as exc:
        raise RuntimeError(
            "Firestore storage requires optional dependencies. Install "
            "requirements-firebase.txt in an environment where its native "
            "dependencies are supported, or set TRUTHLATCH_REGISTRY=memory "
            "for the in-memory prototype."
        ) from exc

    if not firebase_admin._apps:
        key_path_env = os.environ.get("FIREBASE_KEY_PATH")
        if key_path_env:
            key_path = Path(key_path_env).resolve()
        else:
            key_path = (Path(__file__).resolve().parent / "serviceAccountKey.json").resolve()

        if not key_path.is_file():
            raise RuntimeError(f"Firebase service account key not found at {key_path}")

        cred = credentials.Certificate(str(key_path))
        firebase_admin.initialize_app(cred)

    return firestore.client()
