# Job service logic
import uuid
from app.db.models import Job
from app.core.celery_app import celery_app
from app.modules.jobs.tasks import long_running_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def create_job(callback_url: str | None = None):
    db = SessionLocal()
    job_id = str(uuid.uuid4())
    job = Job(id=job_id, status="pending", callback_url=callback_url)
    db.add(job)
    db.commit()
    db.refresh(job)

    long_running_task.apply_async(args=[job_id])  # Enqueue Celery task

    db.close()
    return job_id

def get_job(job_id: str):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()
    return job
