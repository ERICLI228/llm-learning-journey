#!/usr/bin/env python3
"""
Notion 英语口语学习计划创建脚本
自动创建口语学习相关的页面和数据库
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

# 主页 ID（大模型学习计划主页）
MAIN_PAGE_ID = "32d07a3d-e3c3-80d5-8c7e-d5a6244a7afe"

def create_page(title, parent_id, icon=None, content=None):
    """创建页面"""
    url = f"{NOTION_API}/pages"
    data = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        }
    }
    if icon:
        data["icon"] = {"type": "emoji", "emoji": icon}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_database(parent_id, title, properties):
    """创建数据库"""
    url = f"{NOTION_API}/databases"
    data = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [{"text": {"content": title}}],
        "properties": properties
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def add_task_to_database(database_id, task_data):
    """添加任务到数据库"""
    url = f"{NOTION_API}/pages"
    properties = {}
    
    for key, value in task_data.items():
        if key == "任务 ID":
            properties["任务 ID"] = {"title": [{"text": {"content": value}}]}
        elif key == "任务名称":
            properties["任务名称"] = {"rich_text": [{"text": {"content": value}}]}
        elif key == "所属阶段":
            properties["所属阶段"] = {"select": {"name": value}}
        elif key == "周次":
            properties["周次"] = {"select": {"name": value}}
        elif key == "计划开始":
            properties["计划开始"] = {"date": {"start": value}}
        elif key == "计划结束":
            properties["计划结束"] = {"date": {"start": value}}
        elif key == "状态":
            properties["状态"] = {"status": {"name": value}}
        elif key == "优先级":
            properties["优先级"] = {"select": {"name": value}}
    
    data = {"parent": {"database_id": database_id}, "properties": properties}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    print("=" * 70)
    print("🎯 英式口语速成计划 - Notion 自动创建")
    print("=" * 70)
    
    # Step 1: 创建口语学习主页
    print("\n📄 创建口语学习主页...")
    english_page = create_page("🎯 英式口语速成计划", MAIN_PAGE_ID, "🎯")
    
    if "id" not in english_page:
        print(f"❌ 创建失败：{english_page}")
        return
    
    english_page_id = english_page["id"]
    print(f"✅ 口语学习主页已创建")
    print(f"   链接：{english_page.get('url', 'N/A')}")
    
    # Step 2: 创建子页面
    print("\n📁 创建子页面...")
    
    sub_pages = [
        ("📚 术语库", "📚"),
        ("🔊 发音练习", "🔊"),
        ("💬 场景对话", "💬"),
        ("✉️ 邮件模板库", "✉️"),
        ("❌ 错误集锦", "❌"),
        ("📝 每周复盘", "📝"),
        ("🏆 成果集", "🏆"),
    ]
    
    for page_name, icon in sub_pages:
        print(f"  创建：{page_name}...")
        result = create_page(page_name, english_page_id, icon)
        if "id" in result:
            print(f"    ✅ {page_name} 已创建")
        else:
            print(f"    ❌ {page_name} 失败")
    
    # Step 3: 创建术语库子页面
    print("\n📚 创建术语库分类...")
    terms_page = create_page("📚 术语库", english_page_id, "📚")
    if "id" in terms_page:
        terms_page_id = terms_page["id"]
        
        term_categories = [
            ("外贸术语", "🌐"),
            ("物流术语", "🚢"),
            ("供应链术语", "📦"),
            ("自动化术语", "🤖"),
        ]
        
        for cat_name, icon in term_categories:
            cat_page = create_page(cat_name, terms_page_id, icon)
            if "id" in cat_page:
                print(f"  ✅ {cat_name} 已创建")
    
    # Step 4: 创建发音练习子页面
    print("\n🔊 创建发音练习分类...")
    pronunciation_page = create_page("🔊 发音练习", english_page_id, "🔊")
    if "id" in pronunciation_page:
        pron_page_id = pronunciation_page["id"]
        
        pron_categories = [
            ("音标表（44 个）", "🔤"),
            ("连读弱读记录", "🔗"),
            ("语调练习", "📈"),
            ("录音对比", "🎙️"),
        ]
        
        for cat_name, icon in pron_categories:
            cat_page = create_page(cat_name, pron_page_id, icon)
            if "id" in cat_page:
                print(f"  ✅ {cat_name} 已创建")
    
    # Step 5: 创建场景对话子页面
    print("\n💬 创建场景对话分类...")
    dialogue_page = create_page("💬 场景对话", english_page_id, "💬")
    if "id" in dialogue_page:
        dialogue_page_id = dialogue_page["id"]
        
        dialogue_scenes = [
            ("外贸询盘与报价", "💰"),
            ("物流订舱与跟踪", "🚢"),
            ("供应链协调", "🏭"),
            ("自动化体系演示", "💻"),
        ]
        
        for scene_name, icon in dialogue_scenes:
            scene_page = create_page(scene_name, dialogue_page_id, icon)
            if "id" in scene_page:
                print(f"  ✅ {scene_name} 已创建")
    
    # Step 6: 创建每周复盘页面（W1-W12）
    print("\n📝 创建每周复盘页面...")
    review_page = create_page("📝 每周复盘", english_page_id, "📝")
    if "id" in review_page:
        review_page_id = review_page["id"]
        
        for week in range(1, 13):
            week_name = f"Week {week} 复盘"
            week_page = create_page(week_name, review_page_id, "📊")
            if "id" in week_page:
                if week % 3 == 0:  # 每 3 周打印一次
                    print(f"  ✅ {week_name} 已创建")
        print(f"  ✅ Week 1-12 复盘页面已创建")
    
    # Step 7: 添加口语学习任务到主任务数据库
    print("\n📋 添加口语学习任务到主数据库...")
    
    # 主任务数据库 ID
    MAIN_DB_ID = "32d07a3d-e3c3-8155-97a9-d238f7aacc51"
    
    # 阶段一任务（W1-W4）
    phase1_tasks = [
        {"任务 ID": "E1.1", "任务名称": "元音系统学习", "所属阶段": "阶段 1", "周次": "W1", "计划开始": "2026-03-24", "计划结束": "2026-03-30", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E1.2", "任务名称": "辅音系统学习", "所属阶段": "阶段 1", "周次": "W2", "计划开始": "2026-03-31", "计划结束": "2026-04-06", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E1.3", "任务名称": "连读弱读学习", "所属阶段": "阶段 1", "周次": "W3", "计划开始": "2026-04-07", "计划结束": "2026-04-13", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E1.4", "任务名称": "语调与节奏", "所属阶段": "阶段 1", "周次": "W4", "计划开始": "2026-04-14", "计划结束": "2026-04-20", "状态": "⏳ 待开始", "优先级": "🔴 高"},
    ]
    
    # 阶段二任务（W5-W8）
    phase2_tasks = [
        {"任务 ID": "E2.1", "任务名称": "外贸询盘与报价对话", "所属阶段": "阶段 2", "周次": "W5", "计划开始": "2026-04-21", "计划结束": "2026-04-27", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E2.2", "任务名称": "物流订舱与跟踪对话", "所属阶段": "阶段 2", "周次": "W6", "计划开始": "2026-04-28", "计划结束": "2026-05-04", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E2.3", "任务名称": "供应链协调对话", "所属阶段": "阶段 2", "周次": "W7", "计划开始": "2026-05-05", "计划结束": "2026-05-11", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E2.4", "任务名称": "自动化体系演示", "所属阶段": "阶段 2", "周次": "W8", "计划开始": "2026-05-12", "计划结束": "2026-05-18", "状态": "⏳ 待开始", "优先级": "🔴 高"},
    ]
    
    # 阶段三任务（W9-W12）
    phase3_tasks = [
        {"任务 ID": "E3.1", "任务名称": "供应链全链路演讲", "所属阶段": "阶段 3", "周次": "W9", "计划开始": "2026-05-19", "计划结束": "2026-05-25", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E3.2", "任务名称": "模拟商务谈判", "所属阶段": "阶段 3", "周次": "W10", "计划开始": "2026-05-26", "计划结束": "2026-06-01", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E3.3", "任务名称": "公开演讲与问答", "所属阶段": "阶段 3", "周次": "W11", "计划开始": "2026-06-02", "计划结束": "2026-06-08", "状态": "⏳ 待开始", "优先级": "🔴 高"},
        {"任务 ID": "E3.4", "任务名称": "综合考核", "所属阶段": "阶段 3", "周次": "W12", "计划开始": "2026-06-09", "计划结束": "2026-06-15", "状态": "⏳ 待开始", "优先级": "🔴 高"},
    ]
    
    all_tasks = phase1_tasks + phase2_tasks + phase3_tasks
    
    success_count = 0
    for task in all_tasks:
        result = add_task_to_database(MAIN_DB_ID, task)
        if "id" in result:
            success_count += 1
        else:
            print(f"  ❌ {task['任务 ID']}: {task['任务名称']} 失败")
    
    print(f"  ✅ 已添加 {success_count}/{len(all_tasks)} 个口语学习任务")
    
    # 完成
    print("\n" + "=" * 70)
    print("✅ 英式口语速成计划 Notion 配置完成！")
    print("=" * 70)
    print(f"\n📄 口语学习主页：{english_page.get('url', 'N/A')}")
    print("\n📊 已创建:")
    print(f"  - 子页面：{len(sub_pages)} 个")
    print(f"  - 术语库分类：4 个")
    print(f"  - 发音练习分类：4 个")
    print(f"  - 场景对话分类：4 个")
    print(f"  - 每周复盘：12 个")
    print(f"  - 学习任务：{success_count} 个")
    print("\n🎉 现在可以开始英语口语学习了！")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
