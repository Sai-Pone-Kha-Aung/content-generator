#!/usr/bin/env python3

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))
from src.utils.notion_handler import NotionHandler
from config.config import settings

def test_notion_connection():
    print("🧪 Testing Notion Connection...")
    print(f"Notion Token: {settings.notion_token[:10]}..." if settings.notion_token else "No token")
    print(f"Database ID: {settings.notion_database_id}")
    
    try:
        notion = NotionHandler()
        print("✅ NotionHandler initialized")
        
        # Test connection
        connected = notion.test_connection()
        print(f"Connection test: {'✅ Success' if connected else '❌ Failed'}")
        
        if connected:
            # Test database structure
            print("\n🔍 Database structure:")
            structure = notion.get_database_structure()
            for prop_name, prop_details in structure.items():
                prop_type = prop_details.get('type', 'unknown')
                print(f"  - {prop_name}: {prop_type}")
                
        # Test creating a page
        # print("\n📝 Testing page creation...")
        # page_id = notion.create_content_page(
        #     title="Test Page",
        #     content="This is a test content created by the debugging script.",
        #     content_type="Blog",
        #     ai_provider="Debug",
        #     tags=["test", "debug"],
        #     status="Draft"
        # )
        
        # if page_id:
        #     print(f"✅ Page created successfully: {page_id}")
        # else:
        #     print("❌ Failed to create page")
        
        # Test fetching a page
        recent_pages = notion.list_recent_pages(limit=3)
        if recent_pages:
            print(f"✅ Retrieved {len(recent_pages)} recent pages:")
            for i, page in enumerate(recent_pages[:3], 1):
                # Extract page title
                title_prop = page.get('properties', {}).get('Title', {})
                if title_prop.get('title'):
                    title = title_prop['title'][0]['text']['content']
                else:
                    title = "No title"
                
                # Extract page ID
                page_id = page.get('id', 'No ID')
                
                # Extract creation date
                created_time = page.get('created_time', 'Unknown')
                
                print(f"  {i}. {title}")
                print(f"     ID: {page_id}")
                print(f"     Created: {created_time}")
                
                # Show additional properties if available
                properties = page.get('properties', {})
                for prop_name, prop_data in properties.items():
                    if prop_name == 'Title':
                        continue
                    
                    prop_type = prop_data.get('type')
                    if prop_type == 'select' and prop_data.get('select'):
                        value = prop_data['select']['name']
                        print(f"     {prop_name}: {value}")
                    elif prop_type == 'number' and prop_data.get('number') is not None:
                        value = prop_data['number']
                        print(f"     {prop_name}: {value}")
                    elif prop_type == 'rich_text' and prop_data.get('rich_text'):
                        if prop_data['rich_text']:
                            value = prop_data['rich_text'][0]['text']['content'][:50]
                            print(f"     {prop_name}: {value}...")
                    elif prop_type == 'multi_select' and prop_data.get('multi_select'):
                        tags = [tag['name'] for tag in prop_data['multi_select']]
                        print(f"     {prop_name}: {', '.join(tags)}")
                
                print()  # Empty line between pages
        else:
            print("❌ No pages retrieved or retrieval failed")
        
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        

if __name__ == "__main__":
    test_notion_connection()
