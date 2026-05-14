from sqlalchemy.orm import Session
from models import Account, Holding, Transaction, PriceHistory
from schemas import AccountCreate, HoldingCreate, HoldingUpdate, TransactionCreate
from datetime import datetime

def get_accounts(db: Session):
    return db.query(Account).all()

def create_account(db: Session, account: AccountCreate):
    db_account = Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, id: int):
    account = db.query(Account).filter(Account.id == id).first()
    if account:
        db.delete(account)
        db.commit()
        return True
    return False

def get_holdings(db: Session):
    return db.query(Holding).all()

def get_holding(db: Session, id: int):
    return db.query(Holding).filter(Holding.id == id).first()

def create_holding(db: Session, holding: HoldingCreate):
    cost = holding.buy_price * holding.shares
    db_holding = Holding(**holding.dict(), cost=cost)
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

def update_holding(db: Session, id: int, holding: HoldingUpdate):
    db_holding = db.query(Holding).filter(Holding.id == id).first()
    if db_holding:
        update_data = holding.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_holding, key, value)
        db_holding.cost = db_holding.buy_price * db_holding.shares
        db.commit()
        db.refresh(db_holding)
        return db_holding
    return None

def delete_holding(db: Session, id: int):
    holding = db.query(Holding).filter(Holding.id == id).first()
    if holding:
        db.delete(holding)
        db.commit()
        return True
    return False

def get_transactions(db: Session, holding_id: int = None):
    query = db.query(Transaction)
    if holding_id:
        query = query.filter(Transaction.holding_id == holding_id)
    return query.all()

def create_transaction(db: Session, txn: TransactionCreate):
    db_txn = Transaction(**txn.dict())
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn
