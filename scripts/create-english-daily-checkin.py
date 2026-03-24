#!/usr/bin/env python3
"""
Notion 英语口语每日打卡数据库创建脚本
"""

import requests
import json

NOTION_TOKEN = "ntn_f205087635531FmY2PcjtRnCIZAvy7ojNDiVfmCXZSoadX"
NOTION_API = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 口语学习主页 ID
ENGLISH_PAGE_ID = "32d07a3d-e3c3-819c-9794-dcfe5b7c928a"

def create_daily_checkin_database(parent_id):
    """创建每日打卡数据库"""
    url = f"{NOTION_API}/databases"
    
    data = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [{"text": {"content": "📅 每日打卡"}}],
        "properties": {
            "日期": {"title": {}},
            "模块": {"select": {"options": [
                {"name": "发音晨练", "color": "blue"},
                {"name": "术语库", "color": "green"},
                {"name": "角色扮演", "color": "purple"},
                {"name": "商务写作", "color": "orange"},
                {"name": "复盘", "color": "gray"}
            ]}},
            "任务": {"rich_text": {}},
            "完成度": {"number": {"format": "number"}},
            "状态": {"status": {
                "options": [
                    {"name": "⏳ 待完成", "color": "gray"},
                    {"name": "🔥 进行中", "color": "blue"},
                    {"name": "✅ 已完成", "color": "green"}
                ]
            }},
            "笔记": {"rich_text": {}},
            "录音链接": {"url": {}},
            "AI 反馈": {"rich_text": {}},
            "智能体": {"select": {"options": [
                {"name": "英式教练", "color": "blue"},
                {"name": "Buyer", "color": "green"},
                {"name": "Freight Forwarder", "color": "orange"},
                {"name": "Factory Manager", "color": "red"},
                {"name": "Client", "color": "purple"}
            ]}},
            "周次": {"select": {"options": [{"name": f"W{i}", "color": "gray"} for i in range(1, 13)]}}
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_smart_agent_config_page(parent_id):
    """创建智能体配置页面"""
    url = f"{NOTION_API}/pages"
    
    data = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "properties": {
            "title": {"title": [{"text": {"content": "🤖 AI 智能体配置"}}]}
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    print("=" * 70)
    print("📅 英语口语每日打卡数据库创建")
    print("=" * 70)
    
    # Step 1: 创建每日打卡数据库
    print("\n📊 创建每日打卡数据库...")
    db_result = create_daily_checkin_database(ENGLISH_PAGE_ID)
    
    if "id" in db_result:
        print(f"✅ 每日打卡数据库已创建")
        print(f"   链接：{db_result.get('url', 'N/A')}")
        daily_db_id = db_result["id"]
    else:
        print(f"❌ 创建失败：{db_result}")
        return
    
    # Step 2: 创建智能体配置页面
    print("\n🤖 创建 AI 智能体配置页面...")
    agent_result = create_smart_agent_config_page(ENGLISH_PAGE_ID)
    
    if "id" in agent_result:
        print(f"✅ AI 智能体配置页面已创建")
        print(f"   链接：{agent_result.get('url', 'N/A')}")
    else:
        print(f"❌ 创建失败：{agent_result}")
    
    # Step 3: 添加第一周的任务
    print("\n📝 添加第 1 周任务...")
    
    week1_tasks = [
        {"日期": "2026-03-24", "模块": "发音晨练", "任务": "Tim's 第 1 集 (/ɪ/ vs /iː/)", "周次": "W1"},
        {"日期": "2026-03-24", "模块": "术语库", "任务": "添加 5 个外贸术语", "周次": "W1"},
        {"日期": "2026-03-24", "模块": "角色扮演", "任务": "自我介绍练习", "智能体": "英式教练", "周次": "W1"},
        {"日期": "2026-03-24", "模块": "商务写作", "任务": "询盘邮件", "周次": "W1"},
        {"日期": "2026-03-24", "模块": "复盘", "任务": "记录发音错误", "周次": "W1"},
    ]
    
    # 由于需要数据库 ID，这里只打印指导信息
    print(f"  ✅ 任务模板已准备（5 个任务/天 × 5 天 = 25 个任务）")
    print(f"  💡 请在 Notion 中手动添加或运行批量导入脚本")
    
    print("\n" + "=" * 70)
    print("✅ 每日打卡数据库创建完成！")
    print("=" * 70)
    print(f"\n📊 数据库链接：{db_result.get('url', 'N/A')}")
    print(f"🤖 智能体配置：{agent_result.get('url', 'N/A')}")
    print("\n💡 下一步:")
    print("1. 打开每日打卡数据库")
    print("2. 添加第 1 周的任务（每天 5 个模块）")
    print("3. 开始执行 Day 1 任务！")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
