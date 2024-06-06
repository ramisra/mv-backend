import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import event
from sqlmodel import JSON, Column, Field, SQLModel

from core.models.schemas.input_output import ActionInputParameter

TABLE_ACTIONS = "core_actions"


class Visibility(str, Enum):
    public = "public"
    private = "private"


class ActionBase(SQLModel):
    slug: Optional[str] = Field(default=None, unique=True, index=True)

    # This is the front facing name of the action that we will show to the user
    name: str = Field(default=None)
    short_description: str = Field(default="")
    description: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(sa_column=Column(JSON), default_factory=list)
    input_parameters: List[ActionInputParameter] = Field(sa_column=Column(JSON))

    @staticmethod
    def generate_slug(name):
        return name.lower().replace(" ", "-")


class Action(ActionBase, table=True):

    __tablename__ = TABLE_ACTIONS

    # Marked Optional, because you should be able to create an Action without specifying an id
    # The default_factory is used to generate a new UUID if none is provided
    id: Optional[uuid.UUID] = Field(default_factory=lambda: uuid.uuid4(), primary_key=True)

    # This is the internal/modal function name corresponding to this action
    internal_function_name: str = Field(default=None, unique=True)

    # We don't want to expose this field, so we can add it here vs ActionBase
    visibility: Visibility = Field(default=Visibility.public)

    # jobs: List["Job"] = Relationship(back_populates="action")

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class ActionCreate(ActionBase):
    internal_function_name: str


class ActionRead(ActionBase):
    id: uuid.UUID


# @event.listens_for(Action, "before_insert")
# @event.listens_for(Action, "before_update")
# def generate_slug_before_save(mapper, connection, target):
#     target.slug = Action.generate_slug(target.name)


@staticmethod
def get_subtitle_action() -> Optional[Action]:
    return Action(id='b8bc9740-6e5f-428c-ae10-66acb5ccfe0e',
                  internal_function_name='video_captioning',
                  name='video_caption', short_description='Caption your videos',
                  input_parameters=[{"key": "url",
                                     "type": "file_url",
                                     "description": "Your video URL",
                                     "required": True},
                                    {"key": "font_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "font_size",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "font_size",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "font",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "upper_case",
                                     "type": "boolean",
                                     "description": "",
                                     "required": False},
                                    {"key": "shadow_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "shadow_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "border_color",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "border_width",
                                     "type": "text",
                                     "description": "",
                                     "required": False},
                                    {"key": "y_position",
                                     "type": "text",
                                     "description": "",
                                     "required": False}

                                    ]
               )