from sqlalchemy.orm import Session
from models import Holding
import akshare as ak
from datetime import datetime

# 简单内存缓存
_price_cache = {}
_cache_expiry = {}

def get_cached_price(code: str, holding_type: str):
    now = datetime.now().timestamp()
    key = f"{code}_{holding_type}"
    if key in _price_cache and key in _cache_expiry and _cache_expiry[key] > now:
        return _price_cache[key]
    return None

def set_cached_price(code: str, holding_type: str, price: float):
    now = datetime.now().timestamp()
    key = f"{code}_{holding_type}"
    _price_cache[key] = price
    _cache_expiry[key] = now + 300  # 5分钟缓存

def get_market_price(code: str, holding_type: str) -> float:
    cached = get_cached_price(code, holding_type)
    if cached:
        return cached

    price = 0
    try:
        if holding_type == "fund":
            df = ak.fund_open_fund_info_em(symbol=code)
            if not df.empty and len(df) > 0:
                price = float(df.iloc[0]["单位净值"] if "单位净值" in df.columns else df.iloc[0]["净值"])
        elif holding_type == "stock":
            df = ak.stock_zh_a_spot_em()
            row = df[df["代码"] == code]
            if not row.empty:
                price = float(row.iloc[0]["最新价"])
    except Exception:
        pass

    if price > 0:
        set_cached_price(code, holding_type, price)
    return price

def calculate_holding_return(holding: Holding) -> dict:
    market_price = get_market_price(holding.code, holding.type)
    if market_price == 0:
        market_price = holding.current_price if holding.current_price > 0 else holding.buy_price

    current_value = market_price * holding.shares
    profit_loss = current_value - holding.cost
    profit_loss_pct = (profit_loss / holding.cost * 100) if holding.cost > 0 else 0

    return {
        "market_price": market_price,
        "current_value": current_value,
        "profit_loss": profit_loss,
        "profit_loss_pct": profit_loss_pct
    }

def calculate_portfolio_summary(holdings: list) -> dict:
    total_cost = sum(h.cost for h in holdings)
    total_assets = 0
    holdings_data = []

    for h in holdings:
        ret = calculate_holding_return(h)
        total_assets += ret["current_value"]
        holdings_data.append({
            "id": h.id,
            "name": h.name,
            "code": h.code,
            "type": h.type,
            "market_price": ret["market_price"],
            "current_value": ret["current_value"],
            "profit_loss": ret["profit_loss"],
            "profit_loss_pct": ret["profit_loss_pct"]
        })

    total_profit = total_assets - total_cost
    total_profit_pct = (total_profit / total_cost * 100) if total_cost > 0 else 0

    return {
        "total_assets": round(total_assets, 2),
        "total_cost": round(total_cost, 2),
        "total_profit": round(total_profit, 2),
        "total_profit_pct": round(total_profit_pct, 2),
        "holdings_summary": holdings_data
    }

def calculate_asset_allocation(holdings: list) -> dict:
    total_value = sum(calculate_holding_return(h)["current_value"] for h in holdings)
    allocation = {"fund": 0, "stock": 0, "bond": 0}

    for h in holdings:
        val = calculate_holding_return(h)["current_value"]
        allocation[h.type] = round((val / total_value * 100) if total_value > 0 else 0, 2)

    return allocation

def assess_risk_level(holdings: list) -> str:
    if not holdings:
        return "低"

    alloc = calculate_asset_allocation(holdings)
    stock_pct = alloc.get("stock", 0)

    if stock_pct >= 70:
        return "高"
    elif stock_pct >= 40:
        return "中"
    return "低"

def generate_suggestions(holdings: list) -> list:
    suggestions = []

    if not holdings:
        suggestions.append({
            "type": "info",
            "title": "开始投资之旅",
            "content": "添加你的第一笔持仓，开启理财分析之旅！"
        })
        return suggestions

    alloc = calculate_asset_allocation(holdings)
    total = calculate_portfolio_summary(holdings)
    risk = assess_risk_level(holdings)

    # 风险建议
    if risk == "高":
        suggestions.append({
            "type": "warning",
            "title": "风险提示",
            "content": "股票仓位较高（{}%），建议适当配置债券或基金分散风险".format(int(alloc.get("stock", 0)))
        })
    elif risk == "低":
        suggestions.append({
            "type": "info",
            "title": "配置建议",
            "content": "当前风险较低，可适当提高股票仓位追求更高收益"
        })

    # 集中度建议
    if len(holdings) < 3:
        suggestions.append({
            "type": "warning",
            "title": "分散投资",
            "content": "持仓数量较少，建议分散投资降低单一资产风险"
        })

    # 收益率建议
    if total["total_profit_pct"] > 10:
        suggestions.append({
            "type": "success",
            "title": "收益良好",
            "content": "整体收益率 {:.2f}%，表现不错！可考虑适当止盈".format(total["total_profit_pct"])
        })
    elif total["total_profit_pct"] < -5:
        suggestions.append({
            "type": "warning",
            "title": "亏损提醒",
            "content": "当前亏损 {:.2f}%，注意止损，可考虑定投摊薄成本".format(abs(total["total_profit_pct"]))
        })

    # 基金配置建议
    if alloc.get("fund", 0) < 20 and len(holdings) > 0:
        suggestions.append({
            "type": "info",
            "title": "基金配置",
            "content": "建议配置部分指数基金，如沪深300ETF，降低选股风险"
        })

    return suggestions
