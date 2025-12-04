from sqlalchemy.orm import Session

from app.db import models
from app.schemas.tenant import TenantCreate


def create_tenant(db: Session, tenant_in: TenantCreate) -> models.Tenant:
    tenant = models.Tenant(
        name=tenant_in.name,
        code=tenant_in.code,
        is_active=True,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


def get_tenants(db: Session, skip: int = 0, limit: int = 100) -> list[models.Tenant]:
    return db.query(models.Tenant).offset(skip).limit(limit).all()
