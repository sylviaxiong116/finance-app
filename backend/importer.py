import pandas as pd
import io

def parse_csv_content(content: bytes) -> dict:
    """解析 CSV 内容，返回解析结果"""
    results = {"success": [], "failed": [], "errors": []}

    try:
        # 尝试不同编码
        for encoding in ['utf-8', 'gbk', 'gb2312']:
            try:
                text = content.decode(encoding)
                df = pd.read_csv(io.StringIO(text))
                break
            except:
                continue
        else:
            text = content.decode('utf-8', errors='ignore')
            df = pd.read_csv(io.StringIO(text))
    except Exception as e:
        results["errors"].append(f"解析文件失败: {str(e)}")
        return results

    # 列名映射（中英文兼容）
    col_mapping = {
        '名称': 'name', 'name': 'name', '名称': 'name',
        '代码': 'code', 'code': 'code', '股票代码': 'code', '基金代码': 'code',
        '类型': 'type', 'type': 'type',
        '买入价格': 'buy_price', 'buy_price': 'buy_price', '成本价': 'buy_price', '买入价': 'buy_price',
        '持仓数量': 'shares', 'shares': 'shares', '数量': 'shares', '份额': 'shares',
        '买入日期': 'buy_date', 'buy_date': 'buy_date', '日期': 'buy_date'
    }

    df.columns = [col_mapping.get(col.strip(), col.strip()) for col in df.columns]

    # 类型映射
    type_mapping = {'基金': 'fund', '股票': 'stock', '债券': 'bond',
                   'fund': 'fund', 'stock': 'stock', 'bond': 'bond'}

    for idx, row in df.iterrows():
        try:
            name = str(row.get('name', '')).strip()
            code = str(row.get('code', '')).strip()
            htype = str(row.get('type', 'fund')).strip()
            htype = type_mapping.get(htype, 'fund')
            buy_price = float(row.get('buy_price', 0))
            shares = float(row.get('shares', 0))
            buy_date = str(row.get('buy_date', '')).strip() or '2024-01-01'

            if name and code and buy_price > 0 and shares > 0:
                results["success"].append({
                    "name": name,
                    "code": code,
                    "type": htype,
                    "buy_price": buy_price,
                    "shares": shares,
                    "buy_date": buy_date
                })
            else:
                results["failed"].append(f"行 {idx+2}: 数据不完整")
        except Exception as e:
            results["failed"].append(f"行 {idx+2}: {str(e)}")

    return results
