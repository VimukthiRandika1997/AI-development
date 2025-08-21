# API endpoints
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.modules.jobs.service import create_job, get_job

router = APIRouter()

class JobRequest(BaseModel):
    callback_url: str | None = None

class JobResponse(BaseModel):
    job_id: str
    status: str
    result: str | None = None

@router.post("/start-job/", response_model=JobResponse, status_code=202)
def start_job(request: JobRequest):
    job_id = create_job(request.callback_url)
    return JobResponse(job_id=job_id, status="pending", result=None)

@router.get("/status/{job_id}", response_model=JobResponse)
def get_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(job_id=job.id, status=job.status, result=job.result)
