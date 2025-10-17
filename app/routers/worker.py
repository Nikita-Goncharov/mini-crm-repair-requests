from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app import crud, deps, schemas, models
from app.db import get_db

router = APIRouter(prefix="/api/worker", tags=["Worker"])


@router.get("/tickets", response_model=schemas.PagedTickets)
async def list_my_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.require_worker),
):
    total, tickets = await crud.get_tickets_for_worker(db, current_user.id, page, size, search, status)
    return {"meta": {"total": total, "page": page, "size": size}, "items": tickets}


@router.post("/tickets/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: int,
    status: schemas.Status,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.require_worker),
):
    ticket = await crud.get_ticket(db, ticket_id)
    if not ticket or ticket.worker_id != current_user.id:
        raise HTTPException(status_code=404, detail="Ticket not found or unauthorized")
    await crud.update_ticket_status(db, ticket_id, status.value)
    return {"msg": f"Ticket marked as {status.value}"}
