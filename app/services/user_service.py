from sqlalchemy.orm import Session

from app.db import models
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(db: Session, user_in: UserCreate) -> models.User:
    hashed_pw = get_password_hash(user_in.password)
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        tenant_id=user_in.tenant_id,
        campus_id=user_in.campus_id,
        role_id=user_in.role_id,
        hashed_password=hashed_pw,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()
