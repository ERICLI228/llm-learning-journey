#!/bin/bash
# LLM 转型计划 - 配置脚本
# 自动完成所有工具链配置

set -e

echo "🚀 LLM 转型计划 - 配置脚本"
echo "=========================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 GitHub CLI
echo "📦 检查 GitHub CLI..."
if command -v gh &> /dev/null; then
    echo -e "${GREEN}✓ GitHub CLI 已安装${NC}"
    gh --version | head -1
else
    echo -e "${YELLOW}⚠ GitHub CLI 未安装，正在安装...${NC}"
    brew install gh
fi

# GitHub 认证检查
echo ""
echo "🔐 检查 GitHub 认证..."
if gh auth status &> /dev/null; then
    echo -e "${GREEN}✓ GitHub 已认证${NC}"
else
    echo -e "${YELLOW}⚠ GitHub 未认证${NC}"
    echo "请运行以下命令进行认证："
    echo "  gh auth login"
    echo ""
    echo "或者设置 GH_TOKEN 环境变量"
fi

# 创建 GitHub 仓库
echo ""
echo "📁 创建 GitHub 仓库..."
cd ~/.openclaw/workspace/learning/llm-transformation
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git 仓库已初始化${NC}"
else
    git init
    git remote add origin git@github.com:hokeli/llm-learning-journey.git 2>/dev/null || true
    echo -e "${GREEN}✓ Git 仓库已初始化${NC}"
fi

# 检查 Notion CLI
echo ""
echo "📦 检查 Notion CLI..."
if command -v notion &> /dev/null; then
    echo -e "${GREEN}✓ Notion CLI 已安装${NC}"
else
    echo -e "${YELLOW}⚠ Notion CLI 未安装，正在安装...${NC}"
    npm install -g notion-cli
fi

# Notion 认证检查
echo ""
echo "🔐 检查 Notion 认证..."
if [ -n "$NOTION_TOKEN" ]; then
    echo -e "${GREEN}✓ Notion 已认证 (环境变量)${NC}"
else
    echo -e "${YELLOW}⚠ Notion 未认证${NC}"
    echo "请运行以下命令进行认证："
    echo "  notion login"
    echo ""
    echo "或者设置 NOTION_TOKEN 环境变量"
fi

# 检查 Ollama
echo ""
echo "📦 检查 Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama 已安装${NC}"
    ollama --version
else
    echo -e "${YELLOW}⚠ Ollama 未安装${NC}"
    echo "请访问 https://ollama.ai 下载安装"
fi

# 检查本地模型
echo ""
echo "🤖 检查本地模型..."
if command -v ollama &> /dev/null; then
    if ollama list 2>/dev/null | grep -q "qwen2.5"; then
        echo -e "${GREEN}✓ Qwen2.5 模型已下载${NC}"
    else
        echo -e "${YELLOW}⚠ Qwen2.5 模型未下载${NC}"
        echo "请运行以下命令下载："
        echo "  ollama pull qwen2.5:7b"
    fi
fi

# 检查 OpenClaw 配置
echo ""
echo "⚙️ 检查 OpenClaw 配置..."
if openclaw config get models &> /dev/null; then
    echo -e "${GREEN}✓ OpenClaw 模型配置已存在${NC}"
else
    echo -e "${YELLOW}⚠ OpenClaw 模型配置可能不完整${NC}"
fi

# 总结
echo ""
echo "=========================="
echo "📋 配置总结"
echo "=========================="
echo ""
echo "✅ 已完成:"
echo "  - LLM 转型计划文件已创建"
echo "  - 定时提醒已设置"
echo ""
echo "⚠️  需要手动完成:"
echo "  1. GitHub 认证：gh auth login"
echo "  2. 创建 GitHub 仓库并推送代码"
echo "  3. Notion 认证：notion login"
echo "  4. 手动创建 Notion 数据库 (参考 notion-setup.md)"
echo "  5. 手动创建 NotebookLM 知识库 (参考 notebooklm-setup.md)"
echo "  6. Ollama 安装和模型下载 (可选)"
echo ""
echo "📚 下一步:"
echo "  1. 打开 START-HERE.md 查看快速启动指南"
echo "  2. 完成上述手动配置"
echo "  3. 开始 Day 1 学习 (week-01-plan.md)"
echo ""
