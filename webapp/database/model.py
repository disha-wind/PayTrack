from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.inspection import inspect


class Base(DeclarativeBase):
    def to_dict(self, include_relationships=False, exclude=None):
        if exclude is None:
            exclude = []

        data = {}
        for c in inspect(self).mapper.column_attrs:
            if c.key not in exclude:
                value = getattr(self, c.key)
                if isinstance(value, Decimal):
                    value = float(value)
                if isinstance(value, datetime):
                    value = value.isoformat()
                data[c.key] = value

        if include_relationships:
            for rel in inspect(self.__class__).relationships:
                if rel.key not in exclude:
                    value = getattr(self, rel.key)
                    if value is not None:
                        if rel.uselist:
                            data[rel.key] = [item.to_dict() for item in value]
                        else:
                            data[rel.key] = value.to_dict()
        return data

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)

    admin = relationship("Admin", back_populates="user", uselist=False)
    accounts = relationship("Account", back_populates="user")


class Admin(Base):
    __tablename__ = "admin"

    user_id = Column(BigInteger, ForeignKey("user.id"), primary_key=True)

    user = relationship("User", back_populates="admin")


class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    balance = Column(Numeric(precision=12, scale=2), default=0)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="accounts")
    payments = relationship("Payment", back_populates="account")


class Payment(Base):
    __tablename__ = "payment"

    transaction_id = Column(BigInteger, primary_key=True)
    account_id = Column(BigInteger, ForeignKey("account.id"), nullable=False)
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    account = relationship("Account", back_populates="payments")
