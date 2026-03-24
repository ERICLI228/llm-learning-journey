#!/usr/bin/env python3
"""
Notion 数据库自动化创建脚本
使用 Playwright 浏览器自动化
"""

from playwright.sync_api import sync_playwright
import time
import sys

def create_notion_database():
    """自动化创建 Notion 数据库"""
    
    print("🚀 开始自动化创建 Notion 数据库...")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 启动浏览器
        print("\n🌐 启动浏览器...")
        browser = p.chromium.launch(headless=False, args=['--window-size=1280,800'])
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        # 导航到 Notion
        print("\n📄 打开 Notion...")
        page.goto("https://www.notion.so/", wait_until="networkidle")
        time.sleep(3)
        
        # 检查是否已登录
        print("\n🔐 检查登录状态...")
        if "login" in page.url.lower():
            print("⚠️  需要先登录 Notion")
            print("请在浏览器中登录 Notion，然后按 Enter 继续...")
            input()
        
        # 创建新页面
        print("\n📄 创建新页面...")
        print("💡 请在 Notion 中:")
        print("1. 点击左侧边栏的 '+ Add a page' 或 '新建页面'")
        print("2. 输入页面名称：🚀 大模型学习计划")
        print("3. 按 Enter 创建页面")
        print("\n完成后按 Enter 继续...")
        input()
        
        # 获取页面 URL
        page_url = page.url
        print(f"\n✅ 页面已创建：{page_url}")
        
        # 提取页面 ID
        page_id = page_url.split('/')[-1].replace('-', '')
        print(f"📋 页面 ID: {page_id}")
        
        # 连接 Integration
        print("\n🔗 连接 Integration...")
        print("💡 请在 Notion 页面中:")
        print("1. 点击右上角的 '...' (三个点)")
        print("2. 滚动到底部，点击 'Connect to'")
        print("3. 选择 'LLM Learning Assistant'")
        print("\n完成后按 Enter 继续...")
        input()
        
        # 创建数据库
        print("\n📊 创建数据库...")
        print("💡 请在 Notion 页面中:")
        print("1. 输入 '/database' 并选择 'Database - Full page'")
        print("2. 命名数据库：📋 学习任务")
        print("\n完成后按 Enter 继续...")
        input()
        
        # 添加列
        print("\n📝 添加列...")
        print("💡 请添加以下列（按顺序）:")
        columns = [
            ("任务 ID", "Title"),
            ("任务名称", "Text"),
            ("所属阶段", "Select"),
            ("周次", "Select"),
            ("计划开始", "Date"),
            ("计划结束", "Date"),
            ("状态", "Status"),
            ("优先级", "Select"),
            ("预计耗时", "Number"),
            ("使用工具", "Multi-select")
        ]
        
        for i, (name, type_) in enumerate(columns, 1):
            print(f"  {i}. {name} ({type_})")
        
        print("\n完成后按 Enter 继续...")
        input()
        
        # 添加选项
        print("\n🏷️  添加选项...")
        print("💡 请为以下列添加选项:")
        print("\n所属阶段:")
        print("  - 阶段 1 (蓝色)")
        print("  - 阶段 2 (黄色)")
        print("  - 阶段 3 (绿色)")
        print("\n周次:")
        print("  - W1, W2, W3, W4, W5, W6, W7, W8, W9, W10, W11, W12 (灰色)")
        print("\n状态:")
        print("  - ⏳ 待开始 (灰色)")
        print("  - 🔥 进行中 (蓝色)")
        print("  - ✅ 已完成 (绿色)")
        print("  - ❌ 已跳过 (红色)")
        print("\n优先级:")
        print("  - 🔴 高 (红色)")
        print("  - 🟡 中 (黄色)")
        print("  - 🟢 低 (绿色)")
        print("\n使用工具:")
        print("  - OpenClaw, Ollama, Gemini, Qwen, Copilot, LangChain, NotebookLM")
        print("\n完成后按 Enter 继续...")
        input()
        
        # 添加任务
        print("\n✅ 数据库创建完成！")
        print("\n📋 最终信息:")
        print(f"页面 URL: {page.url}")
        print(f"页面 ID: {page_id}")
        
        print("\n💡 下一步:")
        print("1. 在 Notion 中将页面添加到侧边栏（点击页面右侧的 '...' → 'Add to sidebar'）")
        print("2. 关闭浏览器")
        print("3. 将页面 ID 告诉我，我可以帮你添加初始任务数据")
        
        browser.close()

if __name__ == "__main__":
    try:
        create_notion_database()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
