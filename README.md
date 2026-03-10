# Keep Up With Technology (KUWT)

> **An AI-powered content generation pipeline** that keeps technology enthusiasts up-to-date with the latest research, news, and GitHub trends — automatically generating platform-ready posts for LinkedIn, Instagram, Medium, and YouTube, and publishing them directly to **Notion**.

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

The system has transitioned from email distribution to **Notion-based publishing**, allowing for a centralized workspace where content can be reviewed, edited, and scheduled.

Every day, three specialized AI agents run in sequence:

1. **Researchers** — Ingests trending AI research papers from Hugging Face and writes technical content for each paper.
2. **Enthusiasts** — Scrapes the latest technology news and trending GitHub repositories to produce community-focused updates.
3. **Teachers** — Generates educational content about AI/technology fundamentals stored in Redis.

The `AgentOrchestrator` coordinates these agents, normalizes their output into `PostCard` objects, and publishes them to a designated Notion database.

---

## Features

- 🤖 **Three Specialized LangChain Agents** with structured (Pydantic) response formats.
- 📰 **Automated Data Collection**:
  - Research papers from Hugging Face (`HF_TOKEN`).
  - Technology news and trending GitHub repositories (`GITHUB_TOKEN`).
  - Educational topics and history from Redis (Upstash).
- 🎬 **Multi-Platform Content Generation** optimized for LinkedIn, Instagram, Medium, and YouTube.
- 📓 **Notion Integration**: Automatically publishes generated content to a Notion database as drafts for review.
- 🧠 **Flexible LLM Backends**: Mistral (active default), Google Gemini, GitHub OpenAI, and Ollama.
- 💾 **Structured Output**: All agent responses are validated using Pydantic before processing.
- 📁 **Organized Local Storage**: Generated content is also saved as JSON under `src/assets/output/<YYYYMMDD>/`.
- 🔁 **Built-in Resilience**: Includes retry logic and rate-limit safety (60s sleep between calls).

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
    ├── main.py                       # AgentOrchestrator — coordinates pipeline & publishing
    │
    ├── agents/                       # AI agent implementations (Researchers, Teachers, Enthusiasts)
    ├── brains/                       # LLM backend integrations (Mistral, Gemini, etc.)
    ├── models/                       # Pydantic response schemas
    ├── prompts/                      # LLM system prompts
    ├── publishers/                   # Content distribution logic
    │   └── notion_publisher.py       # Notion database integration
    │
    ├── tools/                        # Data collection utilities (HF, GitHub, Redis)
    ├── rendering/                    # Output normalization & formatting
    │   ├── normalize.py              # Logic to build platform-specific PostCards
    │   └── post_digest.py            # PostCard and Platform data models
    │
    ├── utils/                        # Shared utilities (logger, paths, etc.)
    └── assets/
        └── output/                   # Local JSON content storage (by date)
```

---

## Agents

### 1. Researchers Agent (`src/agents/researchers.py`)

Analyzes trending papers from Hugging Face and generates specific content formats for professional and social platforms.

| Platform  | Response Model            |
| --------- | ------------------------- |
| LinkedIn  | `LinkedInResearchPost`    |
| Instagram | `InstagramResearchScript` |
| Medium    | `MediumResearchArticle`   |
| YouTube   | `YouTubeResearchScript`   |

---

### 2. Teachers Agent (`src/agents/teachers.py`)

Creates educational segments based on fundamental topics stored in Redis.

| Platform  | Response Model      |
| --------- | ------------------- |
| LinkedIn  | `LinkedinResponse`  |
| Instagram | `InstagramResponse` |
| Medium    | `MediumResponse`    |
| YouTube   | `YoutubeResponse`   |

---

### 3. Enthusiasts Agent (`src/agents/enthusiasts.py`)

Summarizes trending open-source projects and AI news.

| Platform  | Response Model       |
| --------- | -------------------- |
| LinkedIn  | `LinkedinNewsPost`   |
| Instagram | `InstagramNewsVideo` |
| YouTube   | `YoutubeNewsVideo`   |

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

Your `.env` file should include:

```env
# LLM APIs
MISTRAL_API_KEY=your_key
RESEARCHER_GEMINI=your_key
ENTHUSIAST_GEMINI=your_key
TEACHER_GEMINI=your_key

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

The orchestrator executes agents and publishes to Notion:

```bash
# Set PYTHONPATH to src and run main
PYTHONPATH=src python src/main.py
```

### Main Flow (`src/main.py`)

```python
orchestrator = AgentOrchestrator()
orchestrator.run()         # Executes all agents
orchestrator.publish()     # Normalizes content and pushes to Notion
```

---

## Content Output

### Notion Database

Content is published with the following properties:

- **Name**: The post title.
- **Platform**: LinkedIn, Instagram, Medium, or YouTube.
- **Status**: Set to `Draft` by default.
- **Date**: Today's date.
- **Type**: Research, News & Repos, or Fundamentals.
- **Content**: Full markdown content stored in the page body and a summary field.

### Local Storage

JSON files are saved to `src/assets/output/<YYYYMMDD>/` for backup and debugging.

---

## Technology Stack

| Category            | Library                   |
| ------------------- | ------------------------- |
| **Agent Framework** | `langchain`               |
| **LLMs**            | Mistral AI, Google Gemini |
| **Publisher**       | `notion-client`           |
| **Validation**      | `pydantic`                |
| **Data Sources**    | Redis, BS4, Requests      |
| **Environment**     | `python-dotenv`           |

---

## Todos & Roadmap

See [TODO.md](TODO.md) for detailed tasks.

- [x] Integrate Notion for automated publishing.
- [ ] Implement multi-modal content (image generation for Instagram).
- [ ] Add content scheduling directly from Notion.
- [ ] Expand to Twitter/X and Bluesky.

---

## Contributing

1. Fork the repo.
2. Create your feature branch.
3. Submit a Pull Request.

---

_Built with ❤️ by [Pavan Kumar Balijepalli](https://www.linkedin.com/in/pavan-kumar-balijepalli/) · [Kundelu AI](https://youtube.com/@kundelu-ai)_
