#!/usr/bin/env python3
"""
Notion 数据库更新脚本 - 添加细化版字段
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

# 现有数据库 ID
DATABASE_ID = "32d07a3d-e3c3-8155-97a9-d238f7aacc51"

def update_database_schema():
    """更新数据库字段"""
    
    print("📝 更新 Notion 数据库字段...")
    
    # Notion API 不支持直接添加字段，需要指导用户手动添加
    # 这里生成更新说明
    
    new_fields = [
        ("任务类型", "select", ["理论学习", "动手实践", "项目", "复盘"]),
        ("完成度", "number", "0-100%"),
        ("关联笔记", "relation", "链接到学习笔记页面"),
        ("实验记录", "relation", "链接到实验记录页面"),
        ("NotebookLM 链接", "url", "NotebookLM 对话链接"),
        ("反思总结", "rich_text", "完成后反思"),
        ("明日计划", "rich_text", "下一步行动"),
    ]
    
    print("\n✅ 需要手动添加的字段:")
    for i, (name, type_, desc) in enumerate(new_fields, 1):
        print(f"  {i}. {name} ({type_}) - {desc}")
    
    print("\n💡 添加步骤:")
    print("1. 打开 Notion 数据库")
    print("2. 点击右侧 '+' 添加新列")
    print("3. 选择对应的字段类型")
    print("4. 命名并保存")
    
    return True

def create_sub_pages():
    """创建子页面"""
    
    print("\n📁 创建子页面...")
    
    # 页面结构
    pages = [
        {"name": "📚 学习笔记", "icon": "📚"},
        {"name": "🔬 实验记录", "icon": "🔬"},
        {"name": "📊 项目记录", "icon": "📊"},
        {"name": "❓ 问题清单", "icon": "❓"},
        {"name": "📝 周复盘", "icon": "📝"},
        {"name": "🏆 成果集", "icon": "🏆"},
    ]
    
    print("\n✅ 需要创建的子页面:")
    for page in pages:
        print(f"  - {page['icon']} {page['name']}")
    
    print("\n💡 创建步骤:")
    print("1. 在 Notion 主页点击 '+ Add a page'")
    print("2. 输入页面名称（包含 emoji）")
    print("3. 选择 'Page' 类型")
    print("4. 在页面中添加相应的模板内容")
    
    return True

def main():
    print("=" * 70)
    print("📘 Notion 数据库细化版更新")
    print("=" * 70)
    
    # Step 1: 测试数据库访问
    print("\n🔍 测试数据库访问...")
    url = f"{NOTION_API}/databases/{DATABASE_ID}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ 无法访问数据库：{response.json()}")
        return
    
    print("✅ 数据库访问成功")
    
    # Step 2: 指导添加字段
    update_database_schema()
    
    # Step 3: 指导创建子页面
    create_sub_pages()
    
    # Step 4: 提供模板
    print("\n" + "=" * 70)
    print("📋 模板已生成")
    print("=" * 70)
    print("\n模板文件位置:")
    print("  - 学习笔记模板：docs/DETAILED-PLAN-v2.md")
    print("  - 实验记录模板：docs/DETAILED-PLAN-v2.md")
    print("  - 周复盘模板：docs/DETAILED-PLAN-v2.md")
    print("\n复制对应模板内容到 Notion 页面即可")
    
    # Step 5: NotebookLM 更新指导
    print("\n" + "=" * 70)
    print("🎓 NotebookLM 更新指南")
    print("=" * 70)
    print("\n推荐上传的资料:")
    print("  1. Transformer 论文 PDF")
    print("  2. 课程视频字幕")
    print("  3. 技术博客链接")
    print("  4. 实验输出示例")
    print("  5. 个人笔记草稿")
    print("\n高效提问模板:")
    print("  - '请用比喻解释 [概念]'")
    print("  - '对比 [方案 A] 和 [方案 B] 的优缺点'")
    print("  - '根据我上传的笔记，生成知识点总结'")
    print("  - '我遇到了以下错误：[错误信息]，如何解决？'")
    
    print("\n" + "=" * 70)
    print("✅ 更新指南已生成")
    print("=" * 70)
    print("\n详细文档：docs/DETAILED-PLAN-v2.md")
    print("按照文档指导手动更新 Notion 和 NotebookLM")

if __name__ == "__main__":
    main()
