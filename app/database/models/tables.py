from sqlalchemy import Integer, Column, String, Numeric, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String)


class Firm(Base):
    __tablename__ = "firms"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    paid_for = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user = relationship('User', backref="firms")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    image_id = Column(Integer, unique=True, nullable=False)
    image_uri = Column(String, nullable=False)
    paid_for = Column(Numeric(10, 3))
    payment = Column(Numeric(10, 3))
    previous_debt = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))
    date = Column(Date)

    firm_id = Column(Integer, ForeignKey("firms.id", ondelete="CASCADE"), index=True)
    firm = relationship('Firm', backref='invoices')

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user = relationship('User', backref='invoices')


class Debtor(Base):
    __tablename__ = "debtors"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True)
    paid_for = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user = relationship('User', backref='debtors')


class ShoppingList(Base):
    __tablename__ = "shopping_list"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True)
    purchased = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user = relationship('User', backref='shopping_list')
