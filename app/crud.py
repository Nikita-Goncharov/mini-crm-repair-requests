from sqlalchemy import select, update, delete, func
from app import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy.orm import selectinload


# Users
async def get_user_by_username(db: AsyncSession, username: str):
    q = await db.execute(select(models.User).where(models.User.username == username))
    return q.scalars().first()


async def create_user(db: AsyncSession, user_in: schemas.UserCreate, role: models.Role, hashed_password: str):
    db_user = models.User(
        username=user_in.username, full_name=user_in.full_name, hashed_password=hashed_password, role=role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_workers(db: AsyncSession, skip: int = 0, limit: int = 20):
    q = await db.execute(select(models.User).where(models.User.role == models.Role.worker).offset(skip).limit(limit))
    items = q.unique().scalars().all()
    total = (
        await db.execute(select(func.count(models.User.id)).where(models.User.role == models.Role.worker))
    ).scalar_one()
    return total, items


async def delete_user(db: AsyncSession, user_id: int, role: models.Role):
    await db.execute(delete(models.User).where(models.User.id == user_id, models.User.role == role))
    await db.commit()


# Tickets
async def create_ticket(db: AsyncSession, ticket_in: schemas.TicketCreate):
    client_in = ticket_in.client
    client = models.Client(name=client_in.name, email=client_in.email, phone=client_in.phone)
    db.add(client)
    await db.flush()
    ticket = models.Ticket(title=ticket_in.title, description=ticket_in.description, client_id=client.id)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


async def get_tickets_for_worker(
    db: AsyncSession, worker_id: int, page: int, size: int, search: Optional[str], status: Optional[str]
):
    stmt = (
        select(models.Ticket)
        .options(selectinload(models.Ticket.client), selectinload(models.Ticket.worker))
        .where(models.Ticket.worker_id == worker_id)
    )
    if search:
        stmt = stmt.where(models.Ticket.title.ilike(f"%{search}%"))
    if status:
        stmt = stmt.where(models.Ticket.status == status)
    total = (
        await db.execute(
            select(func.count(models.Ticket.id))
            .where(models.Ticket.worker_id == worker_id)
            .select_from(stmt.subquery())
        )
    ).scalar_one()
    stmt = stmt.offset((page - 1) * size).limit(size)
    res = await db.execute(stmt)
    return total, res.scalars().all()


async def get_tickets_for_admin(db: AsyncSession, page: int, size: int, search: Optional[str], status: Optional[str]):
    stmt = select(models.Ticket).options(selectinload(models.Ticket.client), selectinload(models.Ticket.worker))
    if search:
        stmt = stmt.where(models.Ticket.title.ilike(f"%{search}%"))
    if status:
        stmt = stmt.where(models.Ticket.status == status)
    total = (await db.execute(select(func.count(models.Ticket.id)).select_from(stmt.subquery()))).scalar_one()
    stmt = stmt.offset((page - 1) * size).limit(size)
    res = await db.execute(stmt)
    return total, res.scalars().all()


async def assign_ticket(db: AsyncSession, ticket_id: int, worker_id: int):
    await db.execute(
        update(models.Ticket)
        .where(models.Ticket.id == ticket_id)
        .values(worker_id=worker_id, status=models.Status.assigned)
    )
    await db.commit()


async def update_ticket_status(db: AsyncSession, ticket_id: int, status: str):
    await db.execute(update(models.Ticket).where(models.Ticket.id == ticket_id).values(status=status))
    await db.commit()


async def get_ticket(db: AsyncSession, ticket_id: int):
    q = await db.execute(
        select(models.Ticket)
        .where(models.Ticket.id == ticket_id)
        .options(selectinload(models.Ticket.client), selectinload(models.Ticket.worker))
    )
    return q.scalars().first()
