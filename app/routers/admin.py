from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app import crud, deps, schemas, models
from app.db import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/workers", response_model=schemas.UserRead)
async def create_worker(
    user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db), _: models.User = Depends(deps.require_admin)
):
    existing = await crud.get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = deps.get_password_hash(user_in.password)
    return await crud.create_user(db, user_in, models.Role.worker, hashed_password)


@router.get("/workers", response_model=schemas.PagedUsers)
async def list_workers(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _: models.User = Depends(deps.require_admin),
):
    total, users = await crud.get_workers(db, skip=(page - 1) * size, limit=size)
    return {"meta": {"total": total, "page": page, "size": size}, "items": users}


@router.delete("/workers/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(
    worker_id: int, db: AsyncSession = Depends(get_db), _: models.User = Depends(deps.require_admin)
):
    await crud.delete_user(db, worker_id, models.Role.worker)
    return None


@router.get("/tickets", response_model=schemas.PagedTickets)  # TODO: check pagination
async def list_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _: models.User = Depends(deps.require_admin),
):
    total, tickets = await crud.get_tickets_for_admin(db, page, size, search, status)
    return {"meta": {"total": total, "page": page, "size": size}, "items": tickets}


@router.post("/tickets/{ticket_id}/assign", status_code=status.HTTP_200_OK)
async def assign_ticket(
    ticket_id: int, worker: schemas.WorkerId, db: AsyncSession = Depends(get_db), _: models.User = Depends(deps.require_admin)
):
    await crud.assign_ticket(db, ticket_id, worker.worker_id)
    return {"msg": "Ticket assigned successfully"}
