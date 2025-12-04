from app.db.session import engine
from app.db.base import Base


def init_db() -> None:
    # For now: create tables automatically if they don't exist
    Base.metadata.create_all(bind=engine)
