# Celery tasks
import time
import requests
from app.core.celery_app import celery_app
from app.db.models import Job
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# DB session
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

@celery_app.task(bind=True)
def long_running_task(self, job_id: str):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return

    job.status = "running"
    db.commit()

    # Simulate work
    time.sleep(10)
    result = f"Completed processing job {job_id}"

    job.status = "completed"
    job.result = result
    db.commit()

    # Webhook callback
    if job.callback_url:
        try:
            requests.post(job.callback_url, json={
                "job_id": job_id,
                "status": job.status,
                "result": job.result
            })
        except Exception as e:
            print(f"Webhook failed: {e}")

    db.close()
    return result
