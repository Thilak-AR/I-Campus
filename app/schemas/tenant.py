from datetime import datetime
from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str
    code: str


class TenantCreate(TenantBase):
    pass


class TenantRead(TenantBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True   # for SQLAlchemy 2.x / Pydantic v2
