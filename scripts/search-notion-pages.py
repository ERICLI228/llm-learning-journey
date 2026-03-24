#!/usr/bin/env python3
# Notion 页面搜索脚本

import requests
import json

NOTION_TOKEN = "ntn_f205087635531FmY2PcjtRnCIZAvy7ojNDiVfmCXZSoadX"
NOTION_API = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def search_pages(query=""):
    """搜索页面"""
    url = f"{NOTION_API}/search"
    data = {
        "query": query,
        "filter": {"value": "page", "property": "object"},
        "sort": {"direction": "ascending", "timestamp": "last_edited_time"}
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def main():
    print("🔍 搜索你的 Notion 页面...\n")
    
    results = search_pages("")
    
    if "results" not in results:
        print(f"❌ 搜索失败：{results}")
        return
    
    pages = results["results"]
    
    if not pages:
        print("❌ 没有找到页面")
        print("\n💡 请确保:")
        print("1. Integration 已连接到你的 Notion 工作区")
        print("2. 在 Notion 中点击右上角 '...' → 'Connect to' → 选择你的 Integration")
        return
    
    print(f"✅ 找到 {len(pages)} 个页面/数据库:\n")
    
    for i, page in enumerate(pages[:20], 1):
        title = "Untitled"
        if "title" in page and page["title"]:
            title = page["title"][0].get("plain_text", "Untitled")
        elif "properties" in page and "title" in page["properties"]:
            title_prop = page["properties"]["title"]
            if "title" in title_prop and title_prop["title"]:
                title = title_prop["title"][0].get("plain_text", "Untitled")
        
        page_id = page["id"]
        page_type = page.get("object", "page")
        url = page.get("url", "N/A")
        
        print(f"{i}. 📄 {title}")
        print(f"   ID: {page_id}")
        print(f"   类型：{page_type}")
        print(f"   URL: {url}")
        print()
    
    print("=" * 60)
    print("\n💡 下一步:")
    print("1. 选择一个页面 ID (复制上面的 ID)")
    print("2. 告诉我你想在哪个页面下创建数据库")
    print("3. 或者在 Notion 中新建一个空白页面，然后告诉我 ID")
    print("\n或者你可以:")
    print("1. 在 Notion 中创建一个新页面，命名为 '🚀 大模型学习计划'")
    print("2. 点击右上角 '...' → 'Connect to' → 选择 'LLM Learning Assistant'")
    print("3. 告诉我页面 ID 或 URL")

if __name__ == "__main__":
    main()
