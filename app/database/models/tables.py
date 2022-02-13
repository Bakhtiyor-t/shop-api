from sqlalchemy import Integer, Column, String, Numeric, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship

from ..database import Base


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    users = relationship('User', backref="company")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String)

    company_id = Column(Integer, ForeignKey("company.id", ondelete="SET NULL"))
    chief = Column(Boolean, default=False)


class Firm(Base):
    __tablename__ = "firms"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    # user = relationship('User', backref=backref("firms", cascade="all, delete"))

    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))


class FirmFinance(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    paid = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))
    date = Column(DateTime, nullable=False)

    firm_id = Column(Integer, ForeignKey("firms.id", ondelete="CASCADE"))
    # firm = relationship("Firm", backref=backref("finances", cascade="all, delete"))

    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    image_id = Column(String, unique=True)
    image_uri = Column(String)
    to_pay = Column(Numeric(10, 3))
    paid = Column(Numeric(10, 3))
    previous_debt = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))
    date = Column(DateTime)

    products = relationship("Product", backref="invoice", cascade="all, delete")

    firm_id = Column(Integer, ForeignKey("firms.id", ondelete="CASCADE"), index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)

    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String)
    count = Column(Float)
    type = Column(String)
    price = Column(Numeric(10, 3))
    total_price = Column(Numeric(10, 3))

    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), index=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)


class Debtor(Base):
    __tablename__ = "debtors"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True)
    paid = Column(Numeric(10, 3))
    debt = Column(Numeric(10, 3))

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    # user = relationship('User', backref=backref("debtors", cascade="all, delete"))

    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))


class ShoppingList(Base):
    __tablename__ = "shopping_list"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True)
    purchased = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    # user = relationship('User', backref=backref("shopping_list", cascade="all, delete"))

    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String)  # you can make it unique
    price = Column(Numeric(10, 3))
    date = Column(DateTime)
    firm_flag = Column(Boolean, default=False)

    firm_id = Column(Integer, ForeignKey("firms.id", ondelete="CASCADE"), index=True)
    # firm = relationship('Firm', backref=backref("expenses", cascade="all, delete"))

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    # user = relationship('User', backref=backref("expenses", cascade="all, delete"))

    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))


class CashBox(Base):
    __tablename__ = "cash_box"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    cash = Column(Numeric(10, 3))
    card = Column(Numeric(10, 3))
    date = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    # user = relationship('User', backref=backref("cash_box", cascade="all, delete"))

    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))
    # company = relationship('User', backref=backref("cash_box", cascade="all, delete"))
