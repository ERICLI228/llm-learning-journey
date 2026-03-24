#!/usr/bin/env python3
# Notion 数据库创建脚本 - LLM 转型计划

import requests
import json
from datetime import datetime, timedelta

NOTION_TOKEN = "ntn_f205087635531FmY2PcjtRnCIZAvy7ojNDiVfmCXZSoadX"
NOTION_API = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_page(title, parent_database_id=None, parent_page_id=None):
    """创建页面"""
    if parent_database_id:
        url = f"{NOTION_API}/pages"
        data = {
            "parent": {"database_id": parent_database_id},
            "properties": {
                "任务 ID": {"title": [{"text": {"content": title}}]}
            }
        }
    else:
        url = f"{NOTION_API}/pages"
        data = {
            "parent": {"type": "workspace", "workspace": True},
            "properties": {
                "title": {"title": [{"text": {"content": title}}]}
            }
        }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_database(parent_page_id):
    """创建学习数据库"""
    url = f"{NOTION_API}/databases"
    
    data = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"text": {"content": "🚀 大模型学习计划"}}],
        "properties": {
            "任务 ID": {"title": {}},
            "任务名称": {"rich_text": {}},
            "所属阶段": {"select": {"options": [
                {"name": "阶段 1", "color": "blue"},
                {"name": "阶段 2", "color": "yellow"},
                {"name": "阶段 3", "color": "green"}
            ]}},
            "周次": {"select": {"options": [
                {"name": "W1", "color": "gray"},
                {"name": "W2", "color": "gray"},
                {"name": "W3", "color": "gray"},
                {"name": "W4", "color": "gray"},
                {"name": "W5", "color": "gray"},
                {"name": "W6", "color": "gray"},
                {"name": "W7", "color": "gray"},
                {"name": "W8", "color": "gray"},
                {"name": "W9", "color": "gray"},
                {"name": "W10", "color": "gray"},
                {"name": "W11", "color": "gray"},
                {"name": "W12", "color": "gray"}
            ]}},
            "计划开始": {"date": {}},
            "计划结束": {"date": {}},
            "实际开始": {"date": {}},
            "实际结束": {"date": {}},
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
            "实际耗时": {"number": {"format": "number"}},
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

def add_task_to_database(database_id, task_data):
    """添加任务到数据库"""
    url = f"{NOTION_API}/pages"
    
    properties = {
        "任务 ID": {"title": [{"text": {"content": task_data["id"]}}]},
        "任务名称": {"rich_text": [{"text": {"content": task_data["name"]}}]},
        "所属阶段": {"select": {"name": task_data["phase"]}},
        "周次": {"select": {"name": task_data["week"]}},
        "计划开始": {"date": {"start": task_data["start"]}},
        "计划结束": {"date": {"start": task_data["end"]}},
        "状态": {"status": {"name": "⏳ 待开始"}},
        "优先级": {"select": {"name": task_data.get("priority", "🟡 中")}},
        "预计耗时": {"number": task_data.get("hours", 3)}
    }
    
    if "tools" in task_data:
        properties["使用工具"] = {"multi_select": [{"name": t} for t in task_data["tools"]]}
    
    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    print("🚀 开始创建 Notion 学习数据库...")
    
    # Step 1: 创建主页面
    print("\n📄 创建主页面...")
    page = create_page("🚀 大模型学习计划 (2026.03-2026.06)")
    if "id" not in page:
        print(f"❌ 创建页面失败：{page}")
        return
    page_id = page["id"]
    print(f"✅ 主页面已创建：{page.get('url', 'N/A')}")
    
    # Step 2: 创建数据库
    print("\n📊 创建数据库...")
    db = create_database(page_id)
    if "id" not in db:
        print(f"❌ 创建数据库失败：{db}")
        return
    db_id = db["id"]
    print(f"✅ 数据库已创建：{db.get('url', 'N/A')}")
    
    # Step 3: 添加阶段 1 任务
    print("\n📝 添加阶段 1 任务...")
    phase1_tasks = [
        {"id": "1.1", "name": "Transformer 架构学习", "phase": "阶段 1", "week": "W1", "start": "2026-03-24", "end": "2026-03-26", "priority": "🔴 高", "hours": 8, "tools": ["NotebookLM"]},
        {"id": "1.2", "name": "提示工程掌握", "phase": "阶段 1", "week": "W1", "start": "2026-03-27", "end": "2026-03-30", "priority": "🔴 高", "hours": 6, "tools": ["Gemini", "Qwen"]},
        {"id": "1.3", "name": "本地模型运行 (Ollama)", "phase": "阶段 1", "week": "W2", "start": "2026-03-31", "end": "2026-04-02", "priority": "🟡 中", "hours": 3, "tools": ["Ollama", "OpenClaw"]},
        {"id": "1.4", "name": "API 调用实践", "phase": "阶段 1", "week": "W2", "start": "2026-04-03", "end": "2026-04-05", "priority": "🔴 高", "hours": 4, "tools": ["OpenClaw", "Gemini", "Qwen", "Copilot"]},
        {"id": "1.5", "name": "智能客服原型", "phase": "阶段 1", "week": "W2", "start": "2026-04-06", "end": "2026-04-08", "priority": "🔴 高", "hours": 5, "tools": ["OpenClaw", "Gemini"]},
        {"id": "1.6", "name": "学习管理系统 (Notion + NotebookLM)", "phase": "阶段 1", "week": "W1", "start": "2026-03-24", "end": "2026-03-25", "priority": "🔴 高", "hours": 2, "tools": ["Notion", "NotebookLM"]},
    ]
    
    for task in phase1_tasks:
        result = add_task_to_database(db_id, task)
        if "id" in result:
            print(f"  ✅ 添加任务 {task['id']}: {task['name']}")
        else:
            print(f"  ❌ 添加任务 {task['id']} 失败：{result}")
    
    print("\n✅ Notion 数据库创建完成！")
    print(f"\n📊 数据库链接：{db.get('url', 'N/A')}")
    print(f"📄 主页面链接：{page.get('url', 'N/A')}")
    print("\n💡 下一步:")
    print("1. 在 Notion 中打开数据库查看")
    print("2. 将数据库页面添加到侧边栏")
    print("3. 开始执行 Day 1 任务！")

if __name__ == "__main__":
    main()
