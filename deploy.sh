#!/bin/bash

# 个人理财 Web 应用一键部署脚本
# GitHub 用户名: sylviaxiong116

set -e

echo "======================================"
echo "  个人理财 Web 应用 - 一键部署"
echo "======================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目名称
PROJECT_NAME="finance-app"
GITHUB_USERNAME="sylviaxiong116"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${PROJECT_NAME}.git"

# 部署选项
deploy_local() {
    echo -e "${YELLOW}[1/4] 准备本地部署...${NC}"

    cd "$(dirname "$0")"

    echo -e "${YELLOW}[2/4] 安装后端依赖...${NC}"
    cd backend
    pip install -r requirements.txt

    echo -e "${YELLOW}[3/4] 创建数据库...${NC}"
    mkdir -p /app/data
    python -c "from database import engine, Base; from models import Account; Base.metadata.create_all(bind=engine); print('数据库创建成功')"

    echo -e "${YELLOW}[4/4] 启动服务...${NC}"
    cd ..
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
}

deploy_docker() {
    echo -e "${YELLOW}[1/3] Docker 部署模式${NC}"

    cd "$(dirname "$0")"

    echo -e "${YELLOW}[2/3] 构建 Docker 镜像...${NC}"
    docker build -t ${PROJECT_NAME}:latest .

    echo -e "${YELLOW}[3/3] 启动容器...${NC}"
    docker run -d -p 80:80 --name ${PROJECT_NAME} --restart unless-stopped ${PROJECT_NAME}:latest

    echo -e "${GREEN}部署完成！访问 http://localhost${NC}"
}

deploy_docker_compose() {
    echo -e "${YELLOW}[1/3] Docker Compose 部署模式${NC}"

    cd "$(dirname "$0")"

    echo -e "${YELLOW}[2/3] 使用 Docker Compose 启动...${NC}"
    docker-compose up -d

    echo -e "${GREEN}部署完成！访问 http://localhost${NC}"
}

deploy_github() {
    echo -e "${YELLOW}[1/4] GitHub 部署模式${NC}"

    cd "$(dirname "$0")"

    echo -e "${YELLOW}[2/4] 初始化 Git 仓库...${NC}"
    git init
    git add .
    git commit -m "Initial commit: 个人理财 Web 应用"

    echo -e "${YELLOW}[3/4] 添加远程仓库...${NC}"
    git remote add origin ${REPO_URL}

    echo -e "${YELLOW}[4/4] 推送到 GitHub...${NC}"
    echo -e "${RED}请确保你已经创建了 ${REPO_URL} 仓库${NC}"
    echo -e "${RED}仓库创建地址: https://github.com/new${NC}"
    read -p "按 Enter 继续推送，或 Ctrl+C 取消..."
    git branch -M main
    git push -u origin main

    echo -e "${GREEN}代码已推送到 GitHub！${NC}"
    echo -e "${GREEN}接下来你可以：${NC}"
    echo -e "${GREEN}1. 使用 Render 部署：将 render.yaml 导入${NC}"
    echo -e "${GREEN}2. 使用 Railway 部署：连接此仓库${NC}"
    echo -e "${GREEN}3. 使用 Vercel 部署：连接此仓库${NC}"
}

deploy_render() {
    echo -e "${YELLOW}Render 部署说明${NC}"
    echo "1. 访问 https://render.com 并登录"
    echo "2. 点击 \"New +\" -> \"Blueprint\""
    echo "3. 连接你的 GitHub 仓库"
    echo "4. Render 会自动读取 render.yaml 配置"
    echo "5. 部署完成后访问提供的 URL"
}

# 显示菜单
show_menu() {
    echo ""
    echo "请选择部署方式："
    echo "1) 本地部署 (直接运行)"
    echo "2) Docker 部署"
    echo "3) Docker Compose 部署"
    echo "4) GitHub 推送"
    echo "5) Render 部署说明"
    echo "q) 退出"
    echo ""
}

# 主程序
main() {
    if [ "$#" -eq 0 ]; then
        show_menu
        read -p "请输入选项 [1-5, q]: " choice
    else
        choice=$1
    fi

    case $choice in
        1)
            deploy_local
            ;;
        2)
            deploy_docker
            ;;
        3)
            deploy_docker_compose
            ;;
        4)
            deploy_github
            ;;
        5)
            deploy_render
            ;;
        q|Q)
            echo "退出"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            show_menu
            ;;
    esac
}

# 如果直接运行脚本，执行主程序
# 如果被 source，则提供函数供调用
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
