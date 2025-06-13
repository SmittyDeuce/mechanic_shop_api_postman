from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Date, Float
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Customer(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    
    service_tickets: Mapped[List["ServiceTickets"]] = relationship(back_populates="customer")
    
class ServiceTickets(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String(50), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    service_description: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    
    customer: Mapped["Customer"] = relationship(back_populates="service_tickets")
    service_mechanics: Mapped[List["ServiceMechanics"]] = relationship(back_populates="ticket")

class ServiceMechanics(Base):
    __tablename__ = "service_mechanics"
    
    ticket_id: Mapped[int] = mapped_column(ForeignKey("service_tickets.id"), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("mechanics.id"), primary_key=True)
    
    mechanic: Mapped["Mechanic"] = relationship(back_populates="service_mechanics")
    ticket: Mapped["ServiceTickets"] = relationship(back_populates="service_mechanics")
    
class Mechanic(Base):
    __tablename__ = "mechanics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(Float)
    
    service_mechanics: Mapped[List["ServiceMechanics"]] = relationship(back_populates="mechanic")
    
