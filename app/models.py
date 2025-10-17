from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum
import datetime

Base = declarative_base()


class Role(str, enum.Enum):
    admin = 'admin'
    worker = 'worker'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=True)
    hashed_password = Column(String(200), nullable=False)
    role = Column(Enum(Role), nullable=False)
    tickets = relationship('Ticket', back_populates='worker')


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    tickets = relationship('Ticket', back_populates='client')


class Status(str, enum.Enum):
    new = 'new'
    assigned = 'assigned'
    in_progress = 'in_progress'
    done = 'done'


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(Status), default=Status.new, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    client = relationship('Client', back_populates='tickets')
    worker = relationship('User', back_populates='tickets')
