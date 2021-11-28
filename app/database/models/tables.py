from sqlalchemy import Integer, Column, String, Numeric, ForeignKey, Date

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


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    firm_id = Column(Integer, ForeignKey("firms.id"))
    image_id = Column(Integer, unique=True, nullable=False)
    image_uri = Column(String, nullable=False)
    paid_for = Column(Numeric(10, 3))
    payment = Column(Numeric(10, 3))
    previous_debt = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))
    date = Column(Date)


class Debtor(Base):
    __tablename__ = "debtors"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True)
    paid_for = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))


from sqlalchemy.exc import IntegrityError
