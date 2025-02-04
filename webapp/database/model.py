from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

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
