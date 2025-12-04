from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db import models
from app.db.session import get_db

router = APIRouter(
    prefix="/campuses",
    tags=["campuses"],
)


@router.get("/", response_model=list[dict])
def list_campuses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    campuses = db.query(models.Campus).filter(models.Campus.is_active == True).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "code": c.code,
            "tenant_id": c.tenant_id,
            "is_active": c.is_active,
        }
        for c in campuses
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["SUPER_ADMIN"]))],
)
def create_campus(
    tenant_id: int,
    name: str,
    code: str,
    db: Session = Depends(get_db),
):
    tenant = db.query(models.Tenant).get(tenant_id)
    if not tenant or not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    existing = (
        db.query(models.Campus)
        .filter(
            models.Campus.tenant_id == tenant_id,
            models.Campus.code == code,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campus with same code already exists for this tenant",
        )

    campus = models.Campus(
        tenant_id=tenant_id,
        name=name,
        code=code,
    )
    db.add(campus)
    db.commit()
    db.refresh(campus)
    return {
        "id": campus.id,
        "name": campus.name,
        "code": campus.code,
        "tenant_id": campus.tenant_id,
        "is_active": campus.is_active,
    }
