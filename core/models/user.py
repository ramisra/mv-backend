import uuid
from datetime import datetime
from typing import Optional

import sqlmodel
from sqlalchemy import Column
from sqlmodel import Field, SQLModel

TABLE_USERS = "core_users"


class UserBase(SQLModel):
    name: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    role: str = Field(default="owner")
    user_token: Optional[str] = Field()
    organization_id: Optional[uuid.UUID] = Field(
        sa_column=Column(sqlmodel.UUID, nullable=True), default=uuid.uuid4()
    )
    picture: Optional[str] = Field(
        default=None, sa_column=Column(sqlmodel.AutoString, nullable=True)
    )
    nickname: Optional[str] = Field(
        default=None, sa_column=Column(sqlmodel.AutoString, nullable=True)
    )


class User(UserBase, table=True):

    __tablename__ = TABLE_USERS

    id: Optional[uuid.UUID] = Field(default_factory=lambda: uuid.uuid4(), primary_key=True)
    email_verified: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    # actions: List[Action] = Relationship(back_populates=TABLE_ACTIONS, link_model=Action)

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID
    email_verified: bool = Field(default=False)


class UserUpdate(SQLModel):
    name: Optional[str] = None
    user_token: Optional[str] = None
