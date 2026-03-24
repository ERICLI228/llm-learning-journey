#!/usr/bin/env python3
"""
Notion 数据库半自动化创建脚本
结合 API 和手动步骤
"""

import requests
import json
import time

NOTION_TOKEN = "ntn_f205087635531FmY2PcjtRnCIZAvy7ojNDiVfmCXZSoadX"
NOTION_API = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def search_accessible_pages():
    """搜索可访问的页面"""
    url = f"{NOTION_API}/search"
    data = {"query": "", "page_size": 100}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_database_in_page(page_id):
    """在指定页面中创建数据库"""
    url = f"{NOTION_API}/databases"
    
    data = {
        "parent": {"type": "page_id", "page_id": page_id},
        "title": [{"text": {"content": "📋 学习任务"}}],
        "properties": {
            "任务 ID": {"title": {}},
            "任务名称": {"rich_text": {}},
            "所属阶段": {"select": {"options": [
                {"name": "阶段 1", "color": "blue"},
                {"name": "阶段 2", "color": "yellow"},
                {"name": "阶段 3", "color": "green"}
            ]}},
            "周次": {"select": {"options": [
                {"name": f"W{i}", "color": "gray"} for i in range(1, 13)
            ]}},
            "计划开始": {"date": {}},
            "计划结束": {"date": {}},
            "状态": {"status": {
                "options": [
                    {"name": "⏳ 待开始", "color": "gray"},
                    {"name": "🔥 进行中", "color": "blue"},
                    {"name": "✅ 已完成", "color": "green"},
                    {"name": "❌ 已跳过", "color": "red"}
                ]
            }},
            "优先级": {"select": {"options": [
                {"name": "🔴 高", "color": "red"},
                {"name": "🟡 中", "color": "yellow"},
                {"name": "🟢 低", "color": "green"}
            ]}},
            "预计耗时": {"number": {"format": "number"}},
            "使用工具": {"multi_select": {"options": [
                {"name": "OpenClaw", "color": "blue"},
                {"name": "Ollama", "color": "gray"},
                {"name": "Gemini", "color": "green"},
                {"name": "Qwen", "color": "orange"},
                {"name": "Copilot", "color": "purple"},
                {"name": "LangChain", "color": "pink"},
                {"name": "NotebookLM", "color": "red"}
            ]}},
            "笔记链接": {"relation": {}},
            "代码链接": {"url": {}},
            "验收结果": {"rich_text": {}},
            "遇到的问题": {"rich_text": {}}
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def add_task(database_id, task):
    """添加任务到数据库"""
    url = f"{NOTION_API}/pages"
    
    properties = {
        "任务 ID": {"title": [{"text": {"content": task["id"]}}]},
        "任务名称": {"rich_text": [{"text": {"content": task["name"]}}]},
        "所属阶段": {"select": {"name": task["phase"]}},
        "周次": {"select": {"name": task["week"]}},
        "计划开始": {"date": {"start": task["start"]}},
        "计划结束": {"date": {"start": task["end"]}},
        "状态": {"status": {"name": "⏳ 待开始"}},
        "优先级": {"select": {"name": task.get("priority", "🟡 中")}},
        "预计耗时": {"number": task.get("hours", 3)}
    }
    
    if "tools" in task:
        properties["使用工具"] = {"multi_select": [{"name": t} for t in task["tools"]]}
    
    data = {"parent": {"database_id": database_id}, "properties": properties}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    print("=" * 70)
    print("🚀 Notion 数据库自动化创建")
    print("=" * 70)
    
    # Step 1: 检查当前可访问的页面
    print("\n🔍 检查当前可访问的页面...")
    pages = search_accessible_pages()
    
    if pages.get("results"):
        print(f"\n✅ 找到 {len(pages['results'])} 个可访问的页面:")
        for i, page in enumerate(pages["results"][:10], 1):
            title = "Untitled"
            if "title" in page.get("properties", {}):
                title_prop = page["properties"]["title"]
                if title_prop.get("title"):
                    title = title_prop["title"][0].get("plain_text", "Untitled")
            print(f"  {i}. {title}")
            print(f"     ID: {page['id']}")
            print(f"     URL: {page.get('url', 'N/A')}")
        
        print("\n💡 请选择一个页面 ID 来创建数据库，或者继续下一步创建新页面")
    
    # Step 2: 指导用户创建页面
    print("\n" + "=" * 70)
    print("📄 步骤 1: 在 Notion 中创建页面")
    print("=" * 70)
    print("""
1. 打开 https://www.notion.so/
2. 点击左侧边栏的 "+ Add a page" 或 "新建页面"
3. 输入页面名称：🚀 大模型学习计划
4. 按 Enter 创建页面
5. 点击右上角的 "..." → 滚动到底部 → "Connect to"
6. 选择 "LLM Learning Assistant"
7. 复制页面 URL 或 ID（在 URL 中，32 位字符）
    """)
    
    # 获取用户输入
    page_input = input("\n请输入页面 ID 或 URL (或按 Enter 跳过): ").strip()
    
    if not page_input:
        print("\n⚠️  跳过数据库创建")
        print("你可以稍后手动创建，然后告诉我页面 ID 来添加任务数据")
        return
    
    # 解析页面 ID
    page_id = page_input
    if "notion.so" in page_input:
        # 从 URL 提取 ID
        parts = page_input.rstrip('/').split('/')
        page_id = parts[-1] if parts else page_input
        # 移除连字符
        page_id = page_id.replace('-', '')
    
    # 确保 ID 格式正确（32 位，无连字符）
    page_id = page_id.replace('-', '')
    
    print(f"\n📋 使用页面 ID: {page_id}")
    
    # Step 3: 创建数据库
    print("\n" + "=" * 70)
    print("📊 步骤 2: 创建数据库")
    print("=" * 70)
    print("\n正在创建数据库...")
    
    db_result = create_database_in_page(page_id)
    
    if "id" not in db_result:
        print(f"\n❌ 创建数据库失败")
        print(f"错误：{db_result.get('message', 'Unknown error')}")
        print("\n💡 请确保:")
        print("1. 页面已正确连接到 Integration")
        print("2. 页面 ID 正确")
        return
    
    db_id = db_result["id"]
    db_url = db_result.get("url", "N/A")
    
    print(f"\n✅ 数据库创建成功！")
    print(f"数据库 ID: {db_id}")
    print(f"数据库 URL: {db_url}")
    
    # Step 4: 添加初始任务
    print("\n" + "=" * 70)
    print("📝 步骤 3: 添加初始任务")
    print("=" * 70)
    
    tasks = [
        {"id": "1.1", "name": "Transformer 架构学习", "phase": "阶段 1", "week": "W1", "start": "2026-03-24", "end": "2026-03-26", "priority": "🔴 高", "hours": 8, "tools": ["NotebookLM"]},
        {"id": "1.2", "name": "提示工程掌握", "phase": "阶段 1", "week": "W1", "start": "2026-03-27", "end": "2026-03-30", "priority": "🔴 高", "hours": 6, "tools": ["Gemini", "Qwen"]},
        {"id": "1.3", "name": "本地模型运行 (Ollama)", "phase": "阶段 1", "week": "W2", "start": "2026-03-31", "end": "2026-04-02", "priority": "🟡 中", "hours": 3, "tools": ["Ollama", "OpenClaw"]},
        {"id": "1.4", "name": "API 调用实践", "phase": "阶段 1", "week": "W2", "start": "2026-04-03", "end": "2026-04-05", "priority": "🔴 高", "hours": 4, "tools": ["OpenClaw", "Gemini", "Qwen", "Copilot"]},
        {"id": "1.5", "name": "智能客服原型", "phase": "阶段 1", "week": "W2", "start": "2026-04-06", "end": "2026-04-08", "priority": "🔴 高", "hours": 5, "tools": ["OpenClaw", "Gemini"]},
        {"id": "1.6", "name": "学习管理系统", "phase": "阶段 1", "week": "W1", "start": "2026-03-24", "end": "2026-03-25", "priority": "🔴 高", "hours": 2, "tools": ["Notion", "NotebookLM"]},
    ]
    
    print(f"\n正在添加 {len(tasks)} 个阶段 1 任务...")
    
    for task in tasks:
        result = add_task(db_id, task)
        if "id" in result:
            print(f"  ✅ {task['id']}: {task['name']}")
        else:
            print(f"  ❌ {task['id']}: 失败 - {result.get('message', 'Unknown')}")
    
    # 完成
    print("\n" + "=" * 70)
    print("✅ Notion 数据库配置完成！")
    print("=" * 70)
    print(f"\n📊 数据库链接：{db_url}")
    print("\n💡 下一步:")
    print("1. 在 Notion 中打开数据库查看")
    print("2. 将页面添加到侧边栏（点击 '...' → 'Add to sidebar'）")
    print("3. 开始执行任务！")
    print("\n🎉 加油！3 个月后的你会感谢现在的努力！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
