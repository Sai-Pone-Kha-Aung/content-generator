from notion_client import Client
from typing import Optional, Dict, List, Any
from loguru import logger
from config.config import settings
import re

class NotionHandler:
    def __init__(self):
        if not settings.notion_token:
            raise ValueError("Notion token is not set.")
        
        self.client = Client(auth=settings.notion_token)
        self.database_id = settings.notion_database_id
        logger.info("Notion client initialized successfully.")
        
    def test_connection(self) -> bool:
        """Test Notion API connection"""
        try:
            # Test by retrieving database (remove the token logging)
            logger.info(f"Testing connection to database: {self.database_id}")
            
            db = self.client.databases.retrieve(database_id=self.database_id)
            logger.info("Notion connection successful")
            logger.info(f"Database title: {db.get('title', [{}])[0].get('plain_text', 'No title')}")
            return True
        except Exception as e:
            logger.error(f"Notion connection failed: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            
            # More specific error information
            if hasattr(e, 'status'):
                logger.error(f"HTTP Status: {e.status}")
            if hasattr(e, 'body'):
                logger.error(f"Error body: {e.body}")
                
            return False
        
    def create_content_page(self,
                          title: str,
                          content: str,
                          content_type: str = "Blog",
                          ai_provider: str = "Gemini",
                          tags: List[str] = None,
                          status: str = "Draft") -> Optional[str]:
        """Create a new page in Notion database"""
        try:
            # Calculate word count
            word_count = len(content.split())

            # Prepare tags
            if tags is None:
                tags = []

            # Create page properties
            properties = {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Content": {
                    "rich_text": [
                        {
                            "text": {
                                "content": content[:2000]  # Notion has limits
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": content_type
                    }
                },
                "Status": {
                    "select": {
                        "name": status
                    }
                },
                "AI Model Used": {
                    "rich_text": [
                        {
                            "text": {
                                "content": ai_provider
                            }
                        }
                    ]
                },
                "Word Count": {
                    "number": word_count
                }
            }

            # Add tags if provided
            if tags:
                properties["Tags"] = {
                    "multi_select": [{"name": tag} for tag in tags]
                }

            # Create the page
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )

            page_id = response["id"]
            logger.info(f"Created Notion page: {page_id}")
            return page_id

        except Exception as e:
            logger.error(f"Failed to create Notion page: {e}")
            return None

    def get_database_structure(self) -> Dict:
        """Get database properties for debugging"""
        try:
            db = self.client.databases.retrieve(database_id=self.database_id)
            return db["properties"]
        except Exception as e:
            logger.error(f"Failed to get database structure: {e}")
            return {}

    def list_recent_pages(self, limit: int = 5) -> List[Dict]:
        """Get recent pages from database"""
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                page_size=limit
            )
            logger.info(f"Retrieved {len(response.get('results', []))} pages from database")
            results = response.get("results", [])
            
            return results
        except Exception as e:
            logger.error(f"Failed to list pages: {e}")
            return []