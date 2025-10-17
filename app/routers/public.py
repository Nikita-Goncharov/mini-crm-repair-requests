from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud
from app.db import get_db

router = APIRouter(prefix="/api/public", tags=["Public"])


@router.post("/tickets", response_model=schemas.TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_in: schemas.TicketCreate, db: AsyncSession = Depends(get_db)):
    ticket = await crud.create_ticket(db, ticket_in)
    return ticket
