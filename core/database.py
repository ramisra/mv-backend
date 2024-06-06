from sqlmodel import Session, create_engine

from core.config import get_settings

# connect_args = {"check_same_thread": False}


def get_db_session():
    settings = get_settings()
    engine = create_engine(settings.DATABASE_URI, echo=False)
    with Session(engine) as session:
        yield session

