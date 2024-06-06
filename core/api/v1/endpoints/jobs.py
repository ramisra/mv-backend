import os
import uuid
from typing import Optional

import jinja2

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from starlette.responses import JSONResponse
from pathlib import Path

from core.crud.job import JobCrud
from core.database import get_db_session
from core.models.action import Action
from core.models.job import (
    JobCreate,
    JobRead,
    JobStatusUpdate,
    JobUpdateByUser,
    JobUpdateInternal,
)
from core.models.user import User
from core.services.auth import AuthService

# from core.pubsub import get_pubsub_connection
# from core.services.mail import EmailRequest, send_email

router = APIRouter()

jinja2_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(Path(__file__).parent.parent.parent.parent, "utils/email_templates"))
)


@router.post("/jobs", response_model=JobRead,  dependencies=[Depends(AuthService().is_user_logged_in)])
def create_job(
    job_create_instance: JobCreate,
    current_user: Optional[User] = Depends(AuthService().get_current_user),
    db: Session = Depends(get_db_session),
):
    try:
        return JobCrud.create_job(db, job_create_instance, current_user)
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to submit job: {str(e)}",
            },
            status_code=500,
        )


@router.post("/jobs/update", response_model=JobRead)
async def update_job_status(
    job_update_instance: JobStatusUpdate, db: Session = Depends(get_db_session)
):
    try:
        updated_job = JobCrud.update_job(
            db,
            job_update_instance.id,
            JobUpdateInternal(**job_update_instance.model_dump()),
        )
        if updated_job and updated_job.user_email:
            try:
                job_update_email_template = jinja2_env.get_template(
                    "job_status_update.html"
                )
                job_action = Action.get_subtitle_action(db, updated_job.action_id)
                if not job_action:
                    raise Exception("Job Action not found")
                email_body = job_update_email_template.render(
                    job_status=updated_job.status,
                    job_tracking_link=f"https://www.letsvidify.com/actions/{job_action.slug}?job_id={updated_job.id}",
                    job_output=updated_job.output,
                )
                #await send_email(
                #     EmailRequest(
                #         recipient=updated_job.user_email,
                #         subject=f"Update on Vidify job #{updated_job.id}",
                #         body=email_body,
                #     )
                # )
                # pub_sub_conn = await get_pubsub_connection()
                # if pub_sub_conn:
                #     await pub_sub_conn.publish(
                #         channel=str(updated_job.id),
                #         message=job_update_instance.model_dump_json(),
                #     )
            except Exception as e:  # ignore if the email delivery fails
                print(
                    f"Failed to send email to {updated_job.user_email} for job {updated_job.id} {str(e)}"
                )
        else:
            raise Exception("Failed to update job status, job not found")
        return updated_job
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to update job: {str(e)}",
            },
            status_code=500,
        )


@router.patch("/jobs/{job_id}", response_model=JobRead)
async def update_job_by_user(
    job_id: uuid.UUID,
    job_update_instance: JobUpdateByUser,
    db: Session = Depends(get_db_session),
):
    try:
        updated_job = JobCrud.update_job(
            db, job_id, JobUpdateInternal(**job_update_instance.model_dump())
        )
        return updated_job
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to update job: {str(e)}",
            },
            status_code=500,
        )


@router.get("/jobs/{job_id}", response_model=JobRead)
async def get_job(job_id: uuid.UUID,  current_user: Optional[User] = Depends(AuthService().get_current_user),
                  db: Session = Depends(get_db_session)):
    try:
        job = JobCrud.get_job(db, job_id, current_user)
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
            )
        return job
    except HTTPException as e:
        # If the exception is a 404 error, re-raise it
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise
        # Otherwise, return a generic error response
        return JSONResponse(
            content={
                "status": "error",
                "msg": f"Failed to fetch job with id: {str(job_id)}",
            },
            status_code=500,
        )
