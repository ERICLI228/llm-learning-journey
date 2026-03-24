#!/usr/bin/env python3
"""
Notion 数据库 v2 更新脚本 - 自动添加字段和子页面
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

DATABASE_ID = "32d07a3d-e3c3-8155-97a9-d238f7aacc51"
PARENT_PAGE_ID = "32d07a3d-e3c3-80d5-8c7e-d5a6244a7afe"

def add_property_to_database(property_name, property_config):
    """添加属性到数据库"""
    url = f"{NOTION_API}/databases/{DATABASE_ID}"
    data = {"properties": {property_name: property_config}}
    response = requests.patch(url, json=data, headers=headers)
    return response.json()

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

def main():
    print("=" * 70)
    print("📘 Notion 数据库 v2 自动更新")
    print("=" * 70)
    
    # Step 1: 测试连接
    print("\n🔍 测试数据库连接...")
    url = f"{NOTION_API}/databases/{DATABASE_ID}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ 数据库连接失败：{response.json()}")
        return
    
    db_info = response.json()
    print(f"✅ 数据库连接成功：{db_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")
    
    # Step 2: 添加新字段
    print("\n📝 添加新字段...")
    
    new_properties = {
        "任务类型": {"select": {"options": [
            {"name": "理论学习", "color": "blue"},
            {"name": "动手实践", "color": "green"},
            {"name": "项目", "color": "purple"},
            {"name": "复盘", "color": "orange"}
        ]}},
        "完成度": {"number": {"format": "number"}},
        "NotebookLM 链接": {"url": {}},
        "反思总结": {"rich_text": {}},
        "明日计划": {"rich_text": {}}
    }
    
    for prop_name, prop_config in new_properties.items():
        print(f"  添加字段：{prop_name}...")
        result = add_property_to_database(prop_name, prop_config)
        
        if "id" in result or result.get("status") == 200:
            print(f"    ✅ {prop_name} 添加成功")
        else:
            # 检查是否已存在
            if prop_name in db_info.get("properties", {}):
                print(f"    ⚠️ {prop_name} 已存在")
            else:
                print(f"    ❌ {prop_name} 添加失败：{result}")
    
    # Step 3: 创建子页面
    print("\n📁 创建子页面...")
    
    sub_pages = [
        ("📚 学习笔记", "📚"),
        ("🔬 实验记录", "🔬"),
        ("📊 项目记录", "📊"),
        ("❓ 问题清单", "❓"),
        ("📝 周复盘", "📝"),
        ("🏆 成果集", "🏆"),
    ]
    
    for page_name, icon in sub_pages:
        print(f"  创建页面：{page_name}...")
        result = create_page(page_name, PARENT_PAGE_ID, icon)
        
        if "id" in result:
            print(f"    ✅ {page_name} 创建成功")
            print(f"    链接：{result.get('url', 'N/A')}")
        else:
            print(f"    ❌ {page_name} 创建失败：{result}")
    
    # Step 4: 创建学习笔记子页面
    print("\n📚 创建学习笔记模块页面...")
    
    note_modules = [
        "Transformer 架构",
        "提示工程",
        "API 调用实践",
        "RAG 系统",
        "模型微调",
        "Agent 构建"
    ]
    
    # 先创建学习笔记主页面
    notes_page = create_page("📚 学习笔记", PARENT_PAGE_ID, "📚")
    if "id" in notes_page:
        notes_page_id = notes_page["id"]
        print(f"  ✅ 学习笔记主页面已创建")
        
        # 创建模块子页面
        for module in note_modules:
            print(f"    创建模块：{module}...")
            module_page = create_page(module, notes_page_id, "📖")
            if "id" in module_page:
                print(f"      ✅ {module} 已创建")
    
    # Step 5: 创建周复盘页面
    print("\n📝 创建周复盘页面...")
    
    review_page = create_page("📝 周复盘", PARENT_PAGE_ID, "📝")
    if "id" in review_page:
        review_page_id = review_page["id"]
        print(f"  ✅ 周复盘主页面已创建")
        
        # 创建 W1-W12 子页面
        for week in range(1, 13):
            week_name = f"Week {week} 复盘"
            week_page = create_page(week_name, review_page_id, "📊")
            if "id" in week_page:
                print(f"    ✅ {week_name} 已创建")
    
    print("\n" + "=" * 70)
    print("✅ Notion 数据库 v2 更新完成！")
    print("=" * 70)
    print("\n📊 数据库链接:")
    print(f"https://www.notion.so/{DATABASE_ID.replace('-', '')}")
    print("\n🎉 现在可以开始使用细化版学习计划了！")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
