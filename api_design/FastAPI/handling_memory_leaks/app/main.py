from fastapi import FastAPI, UploadFile, File
from celery import Celery
import shutil
import uuid
import os

# Celery client (only sends tasks)
celery = Celery(
    "pdf_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

app = FastAPI()

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    tmp_id = f"{uuid.uuid4()}.pdf"
    tmp_path = f"/tmp/{tmp_id}"

    # save to a temporary directory
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # send the task to the redis
    celery.send_task("app.worker.process_pdf", args=[tmp_path])

    return {
        "status": "queued",
        "id": tmp_id,
    }
