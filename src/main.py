from agents.researchers import Researchers
from agents.enthusiasts import Enthusiasts
from agents.teachers import Teachers
from datetime import datetime as dt
from utils.logger import log
from utils.paths import ASSETS_OUTPUT_DIR
import os

from rendering.normalize import build_platform_cards
from publishers.notion_publisher import publish_to_notion


class AgentOrchestrator:
    def __init__(self):
        self.researchers = Researchers()
        self.enthusiasts = Enthusiasts()
        self.teachers = Teachers()
        self.date = dt.now().strftime("%Y%m%d")
        self.content = {"researchers": None, "enthusiasts": None, "teachers": None}
        log(f"Initialized Agent Orchestrator for date: {self.date}")

    def run(self):
        # if (ASSETS_OUTPUT_DIR / self.date).exists():
        #     log(
        #         f"Output for date {self.date} already exists. Skipping agent execution."
        #     )
        #     return
        log("Starting Agent Orchestrator...")
        log("Running Researchers Agent...")
        self.content['researchers'] = self.researchers.run()
        log("Running Enthusiasts Agent...")
        self.content['enthusiasts'] = self.enthusiasts.run()
        log("Running Teachers Agent...")
        self.content['teachers'] = self.teachers.run()
        log("All agents have completed their tasks.")

    def publish(self):
        cards_by_platform = build_platform_cards(
            researchers=self.content.get("researchers"),
            enthusiasts=self.content.get("enthusiasts"),
            teachers=self.content.get("teachers"),
        )
        
        publish_to_notion(cards_by_platform, self.date)

    def save_markdown(self):
        cards_by_platform = build_platform_cards(
            researchers=self.content.get("researchers"),
            enthusiasts=self.content.get("enthusiasts"),
            teachers=self.content.get("teachers"),
        )
        out_dir = ASSETS_OUTPUT_DIR / self.date
        out_dir.mkdir(parents=True, exist_ok=True)

        for platform in ["linkedin", "instagram", "medium", "youtube"]:
            cards = cards_by_platform.get(platform) or []
            if not cards:
                continue
            md = "\n\n---\n\n".join([f"## {c.title}\n\n{c.markdown}" for c in cards])
            with (out_dir / f"{platform}.md").open("w", encoding="utf-8") as f:
                f.write(md)


if __name__ == "__main__":
    orchestrator = AgentOrchestrator()
    orchestrator.run()
    orchestrator.publish()
    # orchestrator.save_markdown()
