from sqlmodel import Field, SQLModel
from typing import Union


class ActionInputParameter(SQLModel):
    key: str = Field(default=None)
    type: str = Field(default=None)
    description: str = Field(default=None)
    required: bool = Field(default=True)


class JobInput(SQLModel):
    key: str = Field(default=None)
    value: Union[list, str, dict] = Field(default=None)
