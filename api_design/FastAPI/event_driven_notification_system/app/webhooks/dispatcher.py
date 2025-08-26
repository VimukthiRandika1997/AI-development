# Webhook dispatch logic
from typing import Any, Dict
import json
import hmac
import hashlib
from rq import Queue, Retry
import asyncio
from redis import Redis
from app.core.config import settings
from app.webhooks.utils import fire_webhook
import httpx


# Redis connection & queue for webhooks
redis_conn = Redis.from_url(settings.REDIS_URL)
queue = Queue("webhooks", connection=redis_conn)


async def dispatch_webhook_async(url: str, payload: Dict[str, Any], event_name: str):
    """Utility if you ever want to call the webhook directly in an async context.
    Usually we'll use the worker to perform the HTTP call.
    """
    headers = {"X-Event-Name": event_name}
    if settings.WEBHOOK_SECRET:
        headers["X-Signature"] = sign_payload(settings.WEBHOOK_SECRET, payload)


    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers, timeout=10.0)
        resp.raise_for_status()
        return resp


def run_dispatch_webhook_async(target_url: str, payload: dict, event_type: str):
    """Sync wrapper for dispatch_webhook_async"""
    return asyncio.run(dispatch_webhook_async(target_url, payload, event_type))


def sign_payload(secret: str, payload: Dict[str, Any]) -> str:
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()


def enqueue_webhook_event(target_url: str, payload: dict, event_type: str):
    job = queue.enqueue(
        run_dispatch_webhook_async,
        target_url,
        payload,
        event_type,
        retry=Retry(max=3, interval=[10, 30, 60])
    )
    return job


