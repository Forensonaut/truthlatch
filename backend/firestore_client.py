"""Firestore client initialization and provider for TruthLatch backend."""

import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client


def get_db() -> Client:
    """Return a Firestore client, initializing the Firebase app if not already initialized."""
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
