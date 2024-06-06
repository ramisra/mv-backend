import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import JSON, Column, Field, SQLModel

from core.models.schemas.input_output import JobInput

TABLE_JOBS = "core_jobs"


class JobStatus(str, Enum):
    processing = "processing"
    failed = "failed"
    completed = "completed"


class JobBase(SQLModel):
    action_id: uuid.UUID = Field(foreign_key="core_actions.id", index=True)
    # action: Action = Relationship(back_populates="jobs")

    inputs: List[JobInput] = Field(sa_column=Column(JSON))
    user_email: Optional[str] = Field(default=None, index=False)


class Job(JobBase, table=True):
    __tablename__ = TABLE_JOBS

    id: Optional[uuid.UUID] = Field(default_factory=lambda: uuid.uuid4(), primary_key=True)
    internal_id: Optional[str] = Field(default=None, index=True)
    status: str = Field(default=JobStatus.processing.value)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    # An action function's response will typically be a dict/JSON
    output: Optional[dict] = Field(default={}, sa_column=Column(JSON))
    # Optional because we may in some rare cases want to spin up a job for users that are not logged in
    # Example: For a demo page or a low-cost action
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="core_users.id", index=True)


class JobCreate(JobBase):
    pass


class JobRead(SQLModel):
    output: Optional[dict]
    inputs: Optional[List[JobInput]]
    status: str
    created_at: datetime
    updated_at: datetime
    user_email: Optional[str]


class JobUpdateInternal(SQLModel):
    '''
        Job update payload for crud operations. All updates to job should be
        carried by converting to this model .
    '''
    #TODO(ankush): find way to not set optional and None at the same time
    user_email: Optional[str] = None
    status: Optional[str] = None
    output: Optional[dict] = None


class JobUpdateByUser(SQLModel):
    '''
        Job update payload for end users.
    '''
    user_email: str


class JobStatusUpdate(SQLModel):
    '''
        Job update payload for internal functions.
    '''
    id : uuid.UUID
    status: str
    output: Optional[dict]
