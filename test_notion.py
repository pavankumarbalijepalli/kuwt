import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Load dotenv if available to get variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from publishers.notion_publisher import publish_to_notion
from rendering.email_digest import EmailCard

def test_run():
    # Only try to test if credentials exist
    if not os.environ.get("NOTION_TOKEN") or not os.environ.get("NOTION_DATABASE_ID"):
        print("Error: NOTION_TOKEN or NOTION_DATABASE_ID missing in environment.")
        return
        
    print("Testing Notion Connection...")
        
    dummy_cards = {
        "linkedin": [
            EmailCard(
                title="Test LinkedIn Post",
                source="Research",
                markdown="### Test Heading\nThis is a *test* post generated directly from the Python script to verify the Notion connection.\n\n```python\nprint('Test connection successful')\n```"
            )
        ]
    }
    
    # Run the publisher
    try:
        publish_to_notion(cards_by_platform=dummy_cards, date="20260310")
        print("Test complete. Check your Notion database!")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_run()
