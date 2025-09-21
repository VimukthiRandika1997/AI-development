from celery import Celery
from .ingest import process_pdf_file
import os

celery = Celery(
    "pdf_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery.task(name="app.worker.process_pdf")
def process_pdf(path: str):
    try:
        process_pdf_file(path)
    finally:
        # cleanup file to free disk space
        if os.path.exists(path):
            os.remove(path)
