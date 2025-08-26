# Webhook utility functions
import time
import json
import requests
import hmac
import hashlib
from typing import Dict, Any
from requests import Response
from app.core.config import settings


def sign_payload(secret: str, payload: Dict[str, Any]) -> str:
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()


def fire_webhook(url: str, payload: Dict[str, Any], event_name: str):
    """Synchronous worker function to POST to webhook URL.
    This function is enqueued by RQ. RQ will run it in the worker container.
    """
    headers = {"X-Event-Name": event_name}
    if settings.WEBHOOK_SECRET:
        headers["X-Signature"] = sign_payload(settings.WEBHOOK_SECRET, payload)

    max_attempts = 5
    backoff = 2

    for attempt in range(1, max_attempts + 1):
        try:
            resp: Response = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            # Optionally log success to DB
            return {"status": "delivered", "status_code": resp.status_code}
        except Exception as e:
            # log error (stdout or proper logger)
            print(f"Webhook delivery failed (attempt {attempt}): {e}")
            if attempt == max_attempts:
                # persist failure to a DB or dead-letter queue
                print("Giving up after max attempts")
                return {"status": "failed", "error": str(e)}
            time.sleep(backoff ** attempt)
