from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # alipay, bank, manual
    description = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    holdings = relationship("Holding", back_populates="account", cascade="all, delete-orphan")

class Holding(Base):
    __tablename__ = "holdings"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    type = Column(String(20), nullable=False)  # fund, stock, bond
    buy_price = Column(Float, nullable=False)
    current_price = Column(Float, default=0)
    shares = Column(Float, nullable=False)
    buy_date = Column(String(20), nullable=False)
    cost = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    account = relationship("Account", back_populates="holdings")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    holding_id = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    type = Column(String(20), nullable=False)  # buy, sell, dividend
    shares = Column(Float, default=0)
    price = Column(Float, default=0)
    amount = Column(Float, default=0)
    txn_date = Column(String(20), default="")
    fee = Column(Float, default=0)
    note = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True, index=True)
    holding_id = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    price_date = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    change_pct = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
