from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AccountBase(BaseModel):
    name: str
    type: str
    description: str = ""

class AccountCreate(AccountBase):
    pass

class AccountResponse(AccountBase):
    id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class HoldingBase(BaseModel):
    name: str
    code: str
    type: str
    buy_price: float
    shares: float
    buy_date: str
    account_id: int

class HoldingCreate(HoldingBase):
    pass

class HoldingUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    type: Optional[str] = None
    buy_price: Optional[float] = None
    current_price: Optional[float] = None
    shares: Optional[float] = None
    buy_date: Optional[str] = None

class HoldingResponse(HoldingBase):
    id: int
    cost: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    market_price: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_pct: Optional[float] = None
    current_value: Optional[float] = None
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    holding_id: int
    type: str
    shares: float = 0
    price: float = 0
    amount: float = 0
    txn_date: str = ""
    fee: float = 0
    note: str = ""

class AnalysisSummary(BaseModel):
    total_assets: float
    total_cost: float
    total_profit: float
    total_profit_pct: float
    holdings_summary: List
    asset_allocation: dict
    risk_level: str
    suggestions: List

class ImportResult(BaseModel):
    success: int
    failed: int
    errors: List[str] = []
