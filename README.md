# 个人理财 Web 应用

一款功能完善的个人理财管理 Web 应用，支持持仓管理、实时行情获取、投资分析等功能。

## 功能特性

- **持仓管理**: 添加、编辑、删除基金、股票、债券等持仓
- **实时行情**: 通过 akshare 获取基金和股票实时价格
- **投资分析**: 资产配置分析、风险评估、收益统计
- **数据导入**: 支持 CSV 文件批量导入持仓数据
- **可视化图表**: ECharts 图表展示资产配置和盈亏情况
- **智能建议**: 根据持仓情况提供投资建议

## 技术栈

### 后端
- **FastAPI**: 高性能 Python Web 框架
- **SQLAlchemy**: ORM 数据库访问
- **SQLite**: 轻量级数据库
- **akshare**: 金融数据获取

### 前端
- **React 18**: UI 框架
- **Ant Design 5**: UI 组件库
- **ECharts 5**: 数据可视化
- **纯 HTML/JS**: 无需构建，部署简单

## 项目结构

```
finance-app/
├── backend/
│   ├── main.py              # FastAPI 应用入口
│   ├── database.py          # 数据库配置
│   ├── models.py            # 数据模型
│   ├── schemas.py           # Pydantic 模型
│   ├── crud.py              # 数据库操作
│   ├── analyzer.py          # 投资分析逻辑
│   ├── importer.py          # CSV 导入
│   └── requirements.txt     # Python 依赖
├── frontend/
│   ├── index.html           # 前端页面
│   └── package.json         # 前端配置
├── Dockerfile               # Docker 构建文件
├── docker-compose.yml       # Docker Compose 配置
├── render.yaml              # Render 部署配置
├── vercel.json              # Vercel 配置
├── deploy.sh                # 一键部署脚本
└── README.md                # 项目文档
```

## 快速开始

### 方式一：本地运行

```bash
# 克隆项目
git clone https://github.com/sylviaxiong116/finance-app.git
cd finance-app

# 安装后端依赖
cd backend
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --port 8000

# 访问 http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 方式二：Docker 部署

```bash
# 单容器部署
docker build -t finance-app .
docker run -d -p 80:80 --name finance-app finance-app

# 或使用 Docker Compose
docker-compose up -d
```

访问 http://localhost

### 方式三：云平台部署

#### Render (推荐)
1. Fork 此仓库到你的 GitHub
2. 访问 https://render.com
3. 创建新的 Web Service，选择 "Use existing repo"
4. 选择你的仓库，Render 会自动读取 `render.yaml` 配置
5. 部署完成后获取 URL

#### Railway
1. Fork 此仓库
2. 访问 https://railway.app
3. New Project -> Deploy from GitHub
4. 选择仓库，自动部署

#### Vercel
1. 将代码部署到 GitHub
2. 访问 https://vercel.com
3. Import Project
4. 配置构建命令和输出目录

## API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/holdings` | GET | 获取所有持仓 |
| `/api/holdings` | POST | 添加持仓 |
| `/api/holdings/{id}` | PUT | 更新持仓 |
| `/api/holdings/{id}` | DELETE | 删除持仓 |
| `/api/holdings/accounts` | GET | 获取账户列表 |
| `/api/holdings/accounts` | POST | 创建账户 |
| `/api/analysis/summary` | GET | 获取分析摘要 |
| `/api/import/csv` | POST | 导入 CSV |

## CSV 导入格式

支持中英文列名，示例：

```csv
名称,代码,类型,买入价格,持仓数量,买入日期
沪深300ETF,510300,基金,3.50,1000,2024-01-15
贵州茅台,600519,股票,1800.00,10,2024-03-01
```

支持的类型映射：
- 基金: `fund`
- 股票: `stock`
- 债券: `bond`

## 使用说明

### 添加持仓
1. 点击左侧菜单 "持仓管理"
2. 点击 "+ 添加持仓" 按钮
3. 填写持仓信息（名称、代码、类型、买入价、数量、日期）
4. 选择所属账户
5. 点击确认

### 查看分析
1. 仪表盘页面显示总资产、总收益等概览
2. 饼图展示资产配置比例
3. 柱状图展示各持仓盈亏情况
4. 分析页面提供风险评估和投资建议

### 导入数据
1. 点击 "数据导入"
2. 选择目标账户
3. 上传 CSV 文件
4. 查看导入结果

## 数据存储

默认数据存储位置：`/app/data/finance.db`

可通过环境变量 `DATABASE_DIR` 修改：
```bash
export DATABASE_DIR=/custom/path
```

## 注意事项

1. **akshare 数据源**: 实时行情依赖 akshare，可能受网络和接口限制
2. **数据备份**: 定期备份数据库文件 `finance.db`
3. **安全建议**: 生产环境请配置认证和 HTTPS

## 开发指南

### 本地开发
```bash
# 启动后端（端口 8000）
cd backend
uvicorn main:app --reload

# 前端无需构建，直接打开 frontend/index.html
# 或使用任意静态服务器
python -m http.server 3000 --directory frontend
```

### 运行测试
```bash
cd backend
pytest
```

## License

MIT License

## 联系方式

- GitHub: https://github.com/sylviaxiong116
- Issues: https://github.com/sylviaxiong116/finance-app/issues
