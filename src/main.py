import os
import argparse
from datetime import datetime as dt
from agents.researchers import Researchers
from agents.enthusiasts import Enthusiasts
from agents.teachers import Teachers
from utils.logger import log
from utils.paths import ASSETS_OUTPUT_DIR

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

    def run(self, target_agents=None, target_platforms=None):
        if target_agents is None:
            target_agents = ["researchers", "enthusiasts", "teachers"]

        log(f"Starting Agent Orchestrator for agents: {target_agents} and platforms: {target_platforms}")
        
        agent_map = {
            "researchers": self.researchers.run,
            "enthusiasts": self.enthusiasts.run,
            "teachers": self.teachers.run,
        }

        for agent_name in target_agents:
            if agent_name not in agent_map:
                log(f"Warning: Unknown agent '{agent_name}'. Skipping.")
                continue
                
            try:
                log(f"Running {agent_name.capitalize()} Agent...")
                self.content[agent_name] = agent_map[agent_name](target_platforms=target_platforms)
            except Exception as e:
                log(f"Error running {agent_name} agent: {e}")
        log("Requested agents have completed their tasks.")

    def publish(self, target_platforms=None):
        cards_by_platform = build_platform_cards(
            researchers=self.content.get("researchers"),
            enthusiasts=self.content.get("enthusiasts"),
            teachers=self.content.get("teachers"),
        )
        
        if target_platforms:
            cards_by_platform = {k: v for k, v in cards_by_platform.items() if k in target_platforms}

        publish_to_notion(cards_by_platform, self.date)

    def save_markdown(self, target_platforms=None):
        cards_by_platform = build_platform_cards(
            researchers=self.content.get("researchers"),
            enthusiasts=self.content.get("enthusiasts"),
            teachers=self.content.get("teachers"),
        )
        
        if target_platforms:
            cards_by_platform = {k: v for k, v in cards_by_platform.items() if k in target_platforms}

        out_dir = ASSETS_OUTPUT_DIR / self.date
        out_dir.mkdir(parents=True, exist_ok=True)

        for platform, cards in cards_by_platform.items():
            if not cards:
                continue
            md = "\n\n---\n\n".join([f"## {c.title}\n\n{c.markdown}" for c in cards])
            with (out_dir / f"{platform}.md").open("w", encoding="utf-8") as f:
                f.write(md)


def main():
    parser = argparse.ArgumentParser(description="Run the Agent Orchestrator with selective execution.")
    parser.add_argument(
        "--agents",
        nargs="+",
        choices=["researchers", "enthusiasts", "teachers", "all"],
        default=["all"],
        help="Specific agents to run (default: all)",
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        choices=["linkedin", "instagram", "twitter", "youtube", "all"],
        default=["all"],
        help="Specific platforms to generate for (default: all)",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Automatically publish generated content to Notion",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save generated content as markdown files locally",
    )

    args = parser.parse_args()
    orchestrator = AgentOrchestrator()
    
    target_agents = args.agents
    if "all" in target_agents:
        target_agents = ["researchers", "enthusiasts", "teachers"]

    target_platforms = args.platforms
    if "all" in target_platforms:
        target_platforms = ["linkedin", "instagram", "twitter", "youtube"]

    orchestrator.run(target_agents=target_agents)
    orchestrator.publish(target_platforms=target_platforms)
    
    if args.save:
        orchestrator.save_markdown(target_platforms=target_platforms)


if __name__ == "__main__":
    main()
