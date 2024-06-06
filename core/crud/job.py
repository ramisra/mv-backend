import uuid
from typing import Optional, Sequence

import modal
from sqlmodel import Session, select

from core.config import Settings, get_settings
from core.crud.action import ActionCrud

from core.models.job import Job, JobCreate, JobStatus, JobUpdateInternal
from core.models.user import User

# Todo: Move this to REDIS or something so that it can persist
PENDING_JOBS = {}


class JobCrud:
    def __init__(self):
        pass

    @staticmethod
    def create_job(
            db: Session, job_create_instance: JobCreate,
            user: User,
            settings: Settings = get_settings()
    ) -> Optional[Job]:
        modal_app_name = settings.MODAL_APP_NAME
        job = Job(**job_create_instance.model_dump())
        job.user_id = user.id
        db.add(job)
        db.commit()
        db.refresh(job)

        action = ActionCrud.get_action(db, job.action_id)
        fn = modal.Function.lookup(modal_app_name, action.internal_function_name)

        fn_params = {}
        fn_params["caller_job_id"] = str(job.id)
        for job_input in job_create_instance.inputs:
            fn_params[job_input.key] = job_input.value
        print(fn_params)
        fn_call = fn.spawn(
            **fn_params,
        )

        # TODO(ankush): internal_id is not set, looks like it takes some time.
        job.internal_id = fn_call.get_call_graph()[0].task_id
        db.add(job)
        db.commit()
        # fn_call.resolve() to resolve the function syncrhonously
        # fn_call.get() to get return value of the function
        # print(fn_call)
        # print(dir(fn_call))

        PENDING_JOBS[job.id] = fn_call
        return job

    @staticmethod
    def get_user_job(
            db: Session, user_id: uuid.UUID, user_job_id: uuid.UUID
    ) -> Optional[Job]:
        query = select(Job).where(
            Job.user_id == user_id, Job.id == user_job_id
        )
        return db.exec(query).first()

    @staticmethod
    def get_user_jobs(
        db: Session,
        user: User,
        job_status: JobStatus = JobStatus.processing,
        skip: int = 0,
        limit: int = 10,
    ) -> Sequence[Job]:

        query = select(Job)\
            .where(Job.status == job_status, Job.user_id == user.id).limit(limit)

        data = db.exec(query).all()
        return data

    @staticmethod
    def update_job(
        db: Session, job_id: uuid.UUID, job_update_details: JobUpdateInternal
    ) -> Optional[Job]:
        job = db.get(Job, job_id)
        if job:
            for attr, value in job_update_details.model_dump().items():
                #TODO(ankush): remove the extra none checks
                if attr != "id" and value is not None and hasattr(job,attr):
                    print(f"Updating {attr} with value {value} for job {job_id}")
                    setattr(job, attr, value)
            db.add(job)
            db.commit()
            return job

        return None

    @staticmethod
    def get_job(
            db: Session, job_id: uuid.UUID, user
    ) -> Optional[Job]:
        # adding user None to make sure that the query does not return user
        # generated job.
        query = select(Job).where(
            Job.user_id == user.id, Job.id == job_id
        )
        return db.exec(query).first()
