from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import io

from database import engine, get_db, Base
from models import Account, Holding
from schemas import (
    AccountCreate, AccountResponse,
    HoldingCreate, HoldingUpdate, HoldingResponse,
    TransactionCreate, ImportResult, AnalysisSummary
)
from crud import (
    get_accounts, create_account, delete_account,
    get_holdings, get_holding, create_holding, update_holding, delete_holding,
    get_transactions, create_transaction
)
from analyzer import (
    calculate_portfolio_summary, calculate_asset_allocation,
    assess_risk_level, generate_suggestions, get_market_price
)
from importer import parse_csv_content

# 创建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="个人理财助手 API", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "个人理财助手 API", "docs": "/docs"}

# 账户管理
@app.get("/api/holdings/accounts", response_model=List[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    return get_accounts(db)

@app.post("/api/holdings/accounts", response_model=AccountResponse)
def add_account(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, account)

@app.delete("/api/holdings/accounts/{account_id}")
def remove_account(account_id: int, db: Session = Depends(get_db)):
    if delete_account(db, account_id):
        return {"message": "账户删除成功"}
    raise HTTPException(status_code=404, detail="账户不存在")

# 持仓管理
@app.get("/api/holdings", response_model=List[HoldingResponse])
def list_holdings(db: Session = Depends(get_db)):
    holdings = get_holdings(db)
    result = []
    for h in holdings:
        ret = calculate_portfolio_summary([h])
        data = HoldingResponse.model_validate(h)
        data.market_price = ret["holdings_summary"][0]["market_price"]
        data.current_value = ret["holdings_summary"][0]["current_value"]
        data.profit_loss = ret["holdings_summary"][0]["profit_loss"]
        data.profit_loss_pct = ret["holdings_summary"][0]["profit_loss_pct"]
        result.append(data)
    return result

@app.post("/api/holdings", response_model=HoldingResponse)
def add_holding(holding: HoldingCreate, db: Session = Depends(get_db)):
    return create_holding(db, holding)

@app.put("/api/holdings/{holding_id}", response_model=HoldingResponse)
def edit_holding(holding_id: int, holding: HoldingUpdate, db: Session = Depends(get_db)):
    updated = update_holding(db, holding_id, holding)
    if not updated:
        raise HTTPException(status_code=404, detail="持仓不存在")
    return updated

@app.delete("/api/holdings/{holding_id}")
def remove_holding(holding_id: int, db: Session = Depends(get_db)):
    if delete_holding(db, holding_id):
        return {"message": "持仓删除成功"}
    raise HTTPException(status_code=404, detail="持仓不存在")

@app.get("/api/holdings/refresh-price/{holding_id}")
def refresh_price(holding_id: int, db: Session = Depends(get_db)):
    h = get_holding(db, holding_id)
    if not h:
        raise HTTPException(status_code=404, detail="持仓不存在")
    price = get_market_price(h.code, h.type)
    return {"code": h.code, "market_price": price}

# 分析接口
@app.get("/api/analysis/summary", response_model=AnalysisSummary)
def analysis_summary(db: Session = Depends(get_db)):
    holdings = get_holdings(db)
    summary = calculate_portfolio_summary(holdings)
    return AnalysisSummary(
        total_assets=summary["total_assets"],
        total_cost=summary["total_cost"],
        total_profit=summary["total_profit"],
        total_profit_pct=summary["total_profit_pct"],
        holdings_summary=summary["holdings_summary"],
        asset_allocation=calculate_asset_allocation(holdings),
        risk_level=assess_risk_level(holdings),
        suggestions=generate_suggestions(holdings)
    )

# 导入接口
@app.post("/api/import/csv", response_model=ImportResult)
async def import_csv(
    file: UploadFile = File(...),
    account_id: int = Form(1),
    db: Session = Depends(get_db)
):
    content = await file.read()
    parsed = parse_csv_content(content)

    success_count = 0
    for item in parsed["success"]:
        try:
            holding_data = HoldingCreate(
                account_id=account_id,
                name=item["name"],
                code=item["code"],
                type=item["type"],
                buy_price=item["buy_price"],
                shares=item["shares"],
                buy_date=item["buy_date"]
            )
            create_holding(db, holding_data)
            success_count += 1
        except Exception as e:
            parsed["errors"].append(f"{item['name']}: {str(e)}")

    return ImportResult(
        success=success_count,
        failed=len(parsed["failed"]),
        errors=parsed["errors"]
    )
