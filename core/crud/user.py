import json
import uuid
from typing import Optional, Sequence

from sqlmodel import Session, select

from core.models.user import User, UserCreate, UserUpdate


class UserCrud:

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: uuid.UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        return db.exec(query).first()

    @staticmethod
    def get_user_from_email(db: Session, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        return db.exec(query).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10) -> Sequence[User]:
        query = select(User).offset(skip).limit(limit)
        return db.exec(query).all()

    @staticmethod
    def update_user(db: Session, user: User, updated_user: UserUpdate) -> User:
        for key, value in updated_user.model_dump(exclude_unset=True).items():
            print(key)
            setattr(user, key, value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: uuid.UUID) -> User:
        user = db.get(User, user_id)
        db.delete(user)
        db.commit()
        return user
