# FastAPI entrypoint
import os
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.webhooks.dispatcher import enqueue_webhook_event


app = FastAPI(title="FastAPI Webhook Notifications")


# Example schema
class OrderSchema(BaseModel):
    order_id: int
    user_id: int
    amount: float


@app.post("/order")
async def create_order(order: OrderSchema, background_tasks: BackgroundTasks):
    # imagine saving to DB here (omitted for brevity)
    payload = order.dict()

    # enqueue webhook to a configured URL(s). 
    # In a real app you would lookup subscriber URLs from DB based on event type, user preferences, etc.
    webhook_url = settings.WEBHOOK_TARGET_URL

    # enqueue job to worker (non-blocking)
    enqueue_webhook_event(webhook_url, payload, "order_creation")

    return {"message": "Order received", "order": payload}


@app.get("/")
async def root():
    return {"message": "FastAPI webhook dispatcher is running", "env": settings.APP_ENV}