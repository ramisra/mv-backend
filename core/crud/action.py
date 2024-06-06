import uuid
from typing import Optional, Sequence

from sqlmodel import Session, select

from core.models.action import Action, ActionCreate


class ActionCrud:
    def __init__(self):
        pass

    @staticmethod
    def get_action(db: Session, action_id: uuid.UUID) -> Optional[Action]:
        query = select(Action).where(Action.id == action_id)
        return db.exec(query).first()

    @staticmethod
    def get_action_by_slug(db: Session, slug: str) -> Optional[Action]:
        query = select(Action).where(Action.slug == slug)
        return db.exec(query).first()

    @staticmethod
    def get_actions(
            db: Session, skip: int = 0, limit: int = 10
    ) -> Sequence[Action]:
        query = select(Action).offset(skip).limit(limit)
        return db.exec(query).all()

    @staticmethod
    def create_action(db: Session, action_create: ActionCreate) -> Action:
        action = Action(**action_create.model_dump())
        db.add(action)
        db.commit()
        db.refresh(action)
        return action

    @staticmethod
    def create_quick_action_from_function_name(db: Session, internal_function_name='extract_shorts_from_video_url') -> Action:
        action = Action(
            id=uuid.uuid4(),
            internal_function_name=internal_function_name,
            name=internal_function_name,
            short_description=internal_function_name,
        )
        db.add(action)
        db.commit()
        db.refresh(action)
        return action
