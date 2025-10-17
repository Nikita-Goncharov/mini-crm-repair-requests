from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
import datetime


class Role(str, Enum):
    admin = 'admin'
    worker = 'worker'


class Status(str, Enum):
    new = 'new'
    assigned = 'assigned'
    in_progress = 'in_progress'
    done = 'done'


# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    sub: Optional[str]
    role: Optional[Role]


# User
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str]


class UserRead(BaseModel):
    id: int
    username: str
    role: Role
    full_name: Optional[str]

    class Config:
        from_attributes = True


# Client
class ClientCreate(BaseModel):
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]


class ClientRead(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        from_attributes = True


# Ticket
class TicketCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str]
    client: ClientCreate


class TicketRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: Status
    created_at: datetime.datetime
    client: ClientRead
    worker: Optional[UserRead]

    class Config:
        from_attributes = True


# Pagination
class Page(BaseModel):
    total: int
    page: int
    size: int


class PagedTickets(BaseModel):
    meta: Page
    items: list[TicketRead]


class PagedUsers(BaseModel):
    meta: Page
    items: list[UserRead]


class TicketStatus(BaseModel):
    status: Status

class WorkerId(BaseModel):
    worker_id: int