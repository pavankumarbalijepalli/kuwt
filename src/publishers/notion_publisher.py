import os
import textwrap
from typing import Dict, List
from notion_client import Client
from rendering.post_digest import PostCard, Platform
from utils.logger import log

def publish_to_notion(cards_by_platform: Dict[Platform, List[PostCard]], date: str):
    notion_token = os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not notion_token or not database_id:
        log("Notion credentials not found in environment variables. Skipping publish to Notion.")
        print("Notion credentials not found in environment variables. Skipping publish to Notion.")
        return

    notion = Client(auth=notion_token)
    log(f"Publishing {sum(len(cards) for cards in cards_by_platform.values())} cards to Notion...")

    for platform, cards in cards_by_platform.items():
        for card in cards:
            post_type_map = {
                "Research": "Research",
                "Enthusiast": "News & Repos",
                "Teacher": "Fundamentals"
            }
            content_type = post_type_map.get(card.source, "News")

            try:
                blocks = []
                for chunk in card.markdown.split("\n\n"):
                    chunk = chunk.strip()
                    if not chunk: continue
                    
                    # Notion API limits text content to 2000 characters per block
                    # Handle basic headers and paragraphs
                    
                    # Markdown properties
                    is_code = chunk.startswith("```")
                    if is_code:
                        lines = chunk.split("\n")
                        code_content = "\n".join(lines[1:-1]) if len(lines) > 2 else chunk
                        # split if code is too long
                        for wrapped_chunk in textwrap.wrap(code_content, 2000, replace_whitespace=False):
                            blocks.append({
                                "object": "block",
                                "type": "code",
                                "code": {
                                    "rich_text": [{"type": "text", "text": {"content": wrapped_chunk}}],
                                    "language": "python"
                                }
                            })
                        continue
                        
                    is_header = chunk.startswith("### ")
                    block_type = "heading_3" if is_header else "paragraph"
                    text_content = chunk[4:].strip() if is_header else chunk
                    
                    for wrapped_chunk in textwrap.wrap(text_content, 2000, replace_whitespace=False):
                        blocks.append({
                            "object": "block",
                            "type": block_type,
                            block_type: {
                                "rich_text": [{"type": "text", "text": {"content": wrapped_chunk}}]
                            }
                        })

                # Notion limits block appends to 100 blocks at a time
                block_chunks = [blocks[i:i + 100] for i in range(0, len(blocks), 100)]
                
                formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

                content_rich_text = []
                for chunk in textwrap.wrap(card.markdown, 2000, replace_whitespace=False):
                    content_rich_text.append({"type": "text", "text": {"content": chunk}})

                page = notion.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        "Name": {"title": [{"text": {"content": card.title}}]},
                        "Platform": {"select": {"name": platform}},
                        "Status": {"status": {"name": "Draft"}},
                        "Date": {"date": {"start": formatted_date}},
                        "Type": {"select": {"name": content_type}},
                        "Content": {"rich_text": content_rich_text}
                    },
                    children=block_chunks[0] if block_chunks else []
                )

                for i in range(1, len(block_chunks)):
                    notion.blocks.children.append(
                        block_id=page["id"],
                        children=block_chunks[i]
                    )

                log(f"Successfully published '{card.title}' for {platform} to Notion.")
                print(f"Published to Notion: {platform} - {card.title}")

            except Exception as e:
                log(f"Failed to publish to Notion: {card.title} - {str(e)}")
                print(f"Failed to publish to Notion: {card.title} - {str(e)}")
