from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db import models
from app.db.session import get_db

router = APIRouter(
    prefix="/tenants",
    tags=["tenants"],
)


@router.get("/", response_model=list[dict])
def list_tenants(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tenants = db.query(models.Tenant).filter(models.Tenant.is_active == True).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "code": t.code,
            "is_active": t.is_active,
        }
        for t in tenants
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["SUPER_ADMIN"]))],
)
def create_tenant(
    name: str,
    code: str,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(models.Tenant)
        .filter(
            (models.Tenant.name == name) | (models.Tenant.code == code)
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant with same name or code already exists",
        )

    tenant = models.Tenant(name=name, code=code)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return {
        "id": tenant.id,
        "name": tenant.name,
        "code": tenant.code,
        "is_active": tenant.is_active,
    }


@router.get("/{tenant_id}", response_model=dict)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tenant = db.query(models.Tenant).get(tenant_id)
    if not tenant or not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return {
        "id": tenant.id,
        "name": tenant.name,
        "code": tenant.code,
        "is_active": tenant.is_active,
    }


@router.delete(
    "/{tenant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["SUPER_ADMIN"]))],
)
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
):
    tenant = db.query(models.Tenant).get(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    tenant.is_active = False
    db.add(tenant)
    db.commit()
    return
