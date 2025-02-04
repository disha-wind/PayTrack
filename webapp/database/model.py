from sqlalchemy import Column, BigInteger, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    email = Column(String)
    password_hash = Column(String)
    full_name = Column(String)
    admin = relationship("Admin", back_populates="user", uselist=False)
    accounts = relationship("Account", back_populates="user")

class Admin(Base):
    __tablename__ = "admin"

    user_id = Column(ForeignKey(User.id), primary_key=True)

class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey(User.id))
    balance = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    payments = relationship("Payment", back_populates="payment")

class Payment(Base):
    __tablename__ = "payment"

    transaction_id = Column(BigInteger, primary_key=True)
    account_id = Column(ForeignKey(Account.id))
    amount = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    
