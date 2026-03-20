# Keep Up With Technology (KUWT)

> **An AI-powered content generation pipeline** that keeps technology enthusiasts up-to-date with the latest research, news, and GitHub trends — automatically generating platform-ready posts for LinkedIn, Instagram, Twitter, and YouTube, and publishing them directly to **Notion**.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Agents](#agents)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Content Output](#content-output)
- [Technology Stack](#technology-stack)
- [Todos & Roadmap](#todos--roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**KUWT** (Keep Up With Technology) is an orchestrated multi-agent system that automates the entire lifecycle of technology content creation — from data collection to formatted platform posts ready for review.

The system utilizes an automated **Notion-based publishing** approach, allowing for a centralized workspace where content can be reviewed, edited, and scheduled. It avoids content length limits safely and stores complete responses reliably.

Every day, three specialized AI agents can run:

1. **Researchers** — Ingests trending AI research papers from Hugging Face and writes technical content for each paper.
2. **Enthusiasts** — Scrapes the latest technology news and trending GitHub repositories to produce community-focused updates.
3. **Teachers** — Generates educational content about AI/technology fundamentals stored in Redis.

The `AgentOrchestrator` coordinates these agents, optionally normalizes their output into `PostCard` objects, outputs local Markdown/JSON copies, and publishes them to a designated Notion database.

---

## Features

- 🤖 **Three Specialized LangChain Agents** with structured (Pydantic) response formats.
- 📰 **Automated Data Collection**:
  - Research papers from Hugging Face (`HF_TOKEN`).
  - Technology news and trending GitHub repositories (`GITHUB_TOKEN`).
  - Educational topics and history from Redis (Upstash).
- 🎬 **Multi-Platform Content Generation** optimized for LinkedIn, Instagram, Twitter, and YouTube. (Medium has been deprecated in favor of Twitter threads).
- 📓 **Notion Integration**: Automatically publishes generated content to a Notion database as drafts for review. Automatically handles content chunking to respect database limits.
- 🧠 **Flexible LLM Backends**: Primarily driven by Google Gemini (`gemini-3.1-flash-lite`), efficiently handling long-context inputs and detailed structured output.
- 💾 **Structured Output**: All agent responses are rigorously validated using Pydantic before processing.
- 📁 **Organized Local Storage**: Generated content is saved as JSON and Markdown under `src/assets/output/<YYYYMMDD>/` for backup and auditing.
- 🔁 **Built-in Resilience**: Includes retry logic and rate-limit safety (60s sleep between API calls) to prevent backend exhaustion.
- ⚙️ **Selective Execution Mode**: Leverage token usage efficiently by specifying exact agents and target platforms dynamically via CLI.

---

## Project Architecture

```text
air-kuwt/
├── .env                              # Environment variables
├── .github/
│   └── workflows/
│       └── kuwt.yml                 # GitHub Actions CI/CD workflow
├── requirements.txt
├── TODO.md
├── README.md
└── src/
    ├── main.py                       # AgentOrchestrator — pipeline coordination & CLI execution
    │
    ├── agents/                       # AI agent implementations (Researchers, Teachers, Enthusiasts)
    ├── brains/                       # LLM backend integrations (Gemini, Mistral, etc.)
    ├── models/                       # Pydantic response schemas (LinkedIn, Instagram, Twitter, YouTube)
    ├── prompts/                      # LLM system prompts
    ├── publishers/                   # Content distribution logic
    │   └── notion_publisher.py       # Notion database integration
    │
    ├── tools/                        # Data collection utilities (HF, GitHub, Redis, News)
    ├── rendering/                    # Output normalization & formatting
    │   ├── normalize.py              # Logic to build platform-specific PostCards
    │   └── post_digest.py            # PostCard and Platform data models
    │
    ├── utils/                        # Shared utilities (logger, paths, etc.)
    └── assets/
        └── output/                   # Local JSON/Markdown content storage (by date)
```

---

## Agents

### 1. Researchers Agent (`src/agents/researchers.py`)

Analyzes trending papers from Hugging Face and generates specific content formats for professional and social platforms.

| Platform  | Response Model            |
| --------- | ------------------------- |
| LinkedIn  | `LinkedInPost`            |
| Instagram | `ReelScript`              |
| Twitter   | `TwitterThread`           |
| YouTube   | `YouTubeScript`           |

---

### 2. Teachers Agent (`src/agents/teachers.py`)

Creates educational segments based on fundamental topics stored in Redis. Provides comprehensive coverage tailored to social media lengths.

*Inherits the same robust `LinkedInPost`, `ReelScript`, `TwitterThread`, and `YouTubeScript` models.*

---

### 3. Enthusiasts Agent (`src/agents/enthusiasts.py`)

Summarizes trending open-source projects, global AI updates, and technology news. Ensures all news items are synthesized for quick consumption.

*Inherits the same robust models defined for other agents.*

---

## Installation

### Prerequisites

- Python **3.11+**
- Redis instance (e.g., [Upstash](https://upstash.com/))
- Notion API Token and Database ID

### Setup

1. **Clone and Install:**

   ```bash
   git clone <repository-url>
   cd air-kuwt
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Create a `.env` file in the root (see [Configuration](#configuration)).

---

## Configuration

Your `.env` file should include at minimum:

```env
# LLM APIs
RESEARCHER_GEMINI=your_gemini_api_key
ENTHUSIAST_GEMINI=your_gemini_api_key
TEACHER_GEMINI=your_gemini_api_key

# Notion Integration
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_database_id

# Data Sources
HF_TOKEN=your_huggingface_token
GITHUB_TOKEN=your_github_token
REDIS_URL=your_redis_url
```

---

## Usage

### Run the Pipeline

The orchestrator guarantees flexible generation options. To execute all agents safely for all platforms and publish the output to Notion:

```bash
# Set PYTHONPATH to src and run main
PYTHONPATH=src python src/main.py --agents all --platforms all --publish --save
```

### Advanced Selective Execution

You can target specific platforms and agents to optimize token usage (e.g., bypassing video generation if you only need text feeds). 

```bash
usage: main.py [-h] [--agents] [--platforms] [--publish] [--save]

options:
  -h, --help            show this help message and exit
  --agents {researchers,enthusiasts,teachers,all} [...]
                        Specific agents to run (default: all)
  --platforms {linkedin,instagram,twitter,youtube,all} [...]
                        Specific platforms to generate for (default: all)
  --publish             Automatically publish generated content to Notion
  --save                Save generated content as markdown files locally
```

**Example:** Target just GitHub repositories / News (Enthusiasts) and publish mainly to Twitter and LinkedIn while keeping local backups:

```bash
PYTHONPATH=src python src/main.py --agents enthusiasts --platforms twitter linkedin --publish --save
```

---

## Content Output

### Notion Database

Content is published natively with the following properties:

- **Name**: The post title.
- **Platform**: LinkedIn, Instagram, Twitter, or YouTube.
- **Status**: Set to `Draft` by default.
- **Date**: Today's date.
- **Type**: Research, News & Repos, or Fundamentals.
- **Content**: Full markdown body. (Dynamically formatted to bypass standard Notion length constraints.)

### Local Storage

Both raw JSON outputs and nicely formatted Markdown templates are saved to `src/assets/output/<YYYYMMDD>/`. Use these for backup, debugging, and direct reading without Notion.

---

## Technology Stack

| Category            | Library                   |
| ------------------- | ------------------------- |
| **Agent Framework** | `langchain`               |
| **LLMs**            | Google Gemini             |
| **Publisher**       | `notion-client`           |
| **Validation**      | `pydantic`                |
| **Data Sources**    | Redis, BS4, Requests      |
| **Environment**     | `python-dotenv`           |

---

## Todos & Roadmap

See [TODO.md](TODO.md) for detailed tasks.

- [x] Integrate Notion for automated publishing.
- [x] Allow for efficient cross-platform targeted executions.
- [x] Extend content for Twitter Threads dynamically.
- [ ] Add auto posting for linkedin and X.
- [ ] Implement multi-modal content (image generation for Instagram).
- [ ] Add content scheduling directly from Notion.
- [ ] Expand to Bluesky.

---

## Contributing

1. Fork the repo.
2. Create your feature branch.
3. Submit a Pull Request.

---

_Built with ❤️ by [Pavan Kumar Balijepalli](https://www.linkedin.com/in/pavan-kumar-balijepalli/) · [Kundelu AI](https://youtube.com/@kundelu-ai)_
