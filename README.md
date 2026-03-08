# Keep Up With Technology (KUWT)

> **An AI-powered content generation pipeline** that keeps technology enthusiasts up-to-date with the latest research, news, and GitHub trends — automatically generating platform-ready posts for LinkedIn, Instagram, Medium, and YouTube.

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

**KUWT** (Keep Up With Technology) is an orchestrated multi-agent system that automates the entire lifecycle of technology content creation — from data collection to formatted, email-ready platform posts.

Every day, three specialized AI agents run in sequence:

1. **Researchers** — ingests trending AI research papers from Hugging Face and writes platform-specific content for each paper.
2. **Enthusiasts** — scrapes the latest technology news and trending GitHub repositories to produce community-focused posts.
3. **Teachers** — generates educational content about AI/technology fundamentals stored in Redis.

The `AgentOrchestrator` coordinates all three agents, normalizes their output, renders HTML email digests using Jinja2 templates, and sends platform-specific emails (LinkedIn, Instagram, Medium, YouTube) via Gmail SMTP.

---

## Features

- 🤖 **Three Specialized LangChain Agents** with structured (Pydantic) response formats
- 📰 **Automated Data Collection**
  - Research papers from Hugging Face (`HF_TOKEN`)
  - Technology news and trending GitHub repositories (`GITHUB_TOKEN`)
  - Fundamentals and covered topics from Redis (Upstash)
- 🎬 **Multi-Platform Content Generation** for LinkedIn, Instagram, Medium, and YouTube
- 🧠 **Flexible LLM Backends** — Mistral (active default), Google Gemini, GitHub OpenAI, and Ollama
- 💾 **Pydantic Structured Output** — all agent responses are fully validated before saving
- 📧 **HTML Email Distribution** — styled Jinja2 templates rendered per platform and sent via Gmail SMTP SSL
- 📁 **Organized Output Storage** — generated content saved as JSON and Markdown under `src/assets/output/<YYYYMMDD>/`
- 🔁 **Built-in Retry Logic** — each agent retries up to 3 times on failure
- ⏱️ **Rate-limit Safety** — 60-second sleep between consecutive LLM calls

---

## Project Architecture

```text
air-kuwt/
├── .env                              # Environment variables (not committed)
├── .github/
│   └── workflows/
│       └── kuwt.yml                 # GitHub Actions CI/CD workflow
├── requirements.txt
├── TODO.md
├── README.md
└── src/
    ├── main.py                       # AgentOrchestrator — runs pipeline & sends emails
    │
    ├── agents/                       # AI agent implementations
    │   ├── researchers.py            # Research paper content generator
    │   ├── teachers.py               # Educational fundamentals content generator
    │   └── enthusiasts.py            # Technology news & repos content generator
    │
    ├── brains/                       # LLM backend integrations
    │   ├── mistral.py                # Mistral AI (active default — mistral-large-latest)
    │   ├── gemini.py                 # Google Gemini 2.5 Flash
    │   ├── github_openai.py          # GitHub-hosted OpenAI models
    │   └── ollama.py                 # Local Ollama models
    │
    ├── models/                       # Pydantic response schemas
    │   ├── papers.py                 # Research paper content models
    │   ├── fundamentals.py           # Educational content models
    │   └── tools_and_news.py         # News & repository content models
    │
    ├── prompts/                      # LLM system prompts
    │   ├── papers.py
    │   ├── fundamentals.py
    │   └── tools_and_news.py
    │
    ├── tools/                        # Data collection utilities
    │   ├── fetch_papers.py           # Downloads papers from Hugging Face
    │   ├── fetch_tools_and_news.py   # Fetches AI news and GitHub trending repos
    │   └── fetch_topics.py           # Reads fundamentals topics from Redis
    │
    ├── rendering/                    # Output normalization & HTML email rendering
    │   ├── normalize.py              # Converts agent JSON into platform EmailCards
    │   ├── email_renderer.py         # Jinja2 HTML rendering per platform
    │   ├── email_digest.py           # EmailCard dataclass and Platform type
    │   └── email_templates.py        # Template helpers
    │
    ├── templates/
    │   └── email/                    # Jinja2 HTML email templates (per platform)
    │
    ├── utils/                        # Utility functions
    │   ├── email_handler.py          # Gmail SMTP SSL email sender
    │   ├── logger.py                 # File-based logging
    │   ├── paths.py                  # Centralized path constants
    │   ├── json_tree.py              # JSON processing utilities
    │   └── stt.py                    # Speech-to-text utilities
    │
    └── assets/
        ├── input/                    # (Legacy) JSON input fallback files
        │   └── papers/               # Downloaded research papers (by date)
        └── output/                   # Generated content (organized by date)
            └── <YYYYMMDD>/
                ├── researchers.json
                ├── teachers.json
                ├── enthusiasts.json
                └── *.md              # Optional markdown exports

logs/                                 # Application log files
```

---

## Agents

### 1. Researchers Agent (`src/agents/researchers.py`)

Reads trending research papers fetched from Hugging Face and generates platform-specific content for each paper.

| Platform  | Agent Name                | Response Model            |
| --------- | ------------------------- | ------------------------- |
| LinkedIn  | `researcher_on_linkedin`  | `LinkedInResearchPost`    |
| Instagram | `researcher_on_instagram` | `InstagramResearchScript` |
| Medium    | `researcher_on_medium`    | `MediumResearchArticle`   |
| YouTube   | `researcher_on_youtube`   | `YouTubeResearchScript`   |

- Input: paper text from `tools/fetch_papers.py`
- Output: `src/assets/output/<date>/researchers.json`
- Rate limit: 60s sleep between each platform call per paper

---

### 2. Teachers Agent (`src/agents/teachers.py`)

Generates educational content on AI/technology fundamentals by calling the `fetch_topics` tool (backed by Redis).

| Platform  | Agent Name             | Response Model      |
| --------- | ---------------------- | ------------------- |
| LinkedIn  | `teacher_on_linkedin`  | `LinkedinResponse`  |
| Instagram | `teacher_on_instagram` | `InstagramResponse` |
| Medium    | `teacher_on_medium`    | `MediumResponse`    |
| YouTube   | `teacher_on_youtube`   | `YoutubeResponse`   |

- Input: fundamentals topic fetched via Redis (`fundamentals` key)
- Output: `src/assets/output/<date>/teachers.json`

---

### 3. Enthusiasts Agent (`src/agents/enthusiasts.py`)

Scrapes technology news and trending GitHub repositories to generate community-focused posts.

| Platform  | Agent Name                | Response Model       |
| --------- | ------------------------- | -------------------- |
| LinkedIn  | `enthusiast_on_linkedin`  | `LinkedinNewsPost`   |
| Instagram | `enthusiast_on_instagram` | `InstagramNewsVideo` |
| YouTube   | `enthusiast_on_youtube`   | `YoutubeNewsVideo`   |

- Input: news and repos from `tools/fetch_tools_and_news.py`
- Output: `src/assets/output/<date>/enthusiasts.json`

> **Note:** Medium posts are not currently generated by the Enthusiasts agent.

---

### Agent Orchestrator (`src/main.py`)

The `AgentOrchestrator` class coordinates all three agents:

```python
orchestrator = AgentOrchestrator()
orchestrator.run()         # Runs all three agents sequentially
orchestrator.send_email()  # Renders HTML and sends 4 platform emails
```

It also exposes `save_markdown()` to export platform content as `.md` files (disabled by default in `__main__`).

---

## Installation

### Prerequisites

- Python **3.11+**
- Git
- Active accounts/API keys for: Mistral AI, Hugging Face, GitHub, Gmail SMTP
- A Redis instance (e.g. [Upstash](https://upstash.com/)) with `fundamentals` and `covered` keys populated

### Setup

1. **Clone the repository:**

```bash
git clone <repository-url>
cd air-kuwt
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables** (see [Configuration](#configuration) below).

5. **Seed Redis** with fundamental topics and covered content (required for the Teachers agent).

---

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# ── LLM APIs ──────────────────────────────────────────────────────────────────
MISTRAL_API_KEY=<your-mistral-api-key>          # Active LLM — all agents use this
RESEARCHER_GEMINI=<your-gemini-api-key>         # Optional: Google Gemini backend
TEACHER_GEMINI=<your-gemini-api-key>            # Optional: Google Gemini backend
ENTHUSIAST_GEMINI=<your-gemini-api-key>         # Optional: Google Gemini backend
GITHUB_TOKEN=<your-github-pat>                  # For GitHub trending repo fetching

# ── Data Sources ──────────────────────────────────────────────────────────────
HF_TOKEN=<your-huggingface-token>               # For fetching trending research papers
REDIS_URL=<your-redis-url>                      # Upstash (or any Redis) connection string
                                                # Keys required: `fundamentals`, `covered`

# ── Email Distribution (Gmail SMTP SSL) ───────────────────────────────────────
EMAIL_FROM=<your-gmail-address>
EMAIL_PASSWORD=<your-gmail-app-password>        # Gmail App Password (not account password)
EMAIL_TO=<recipient-email-or-group>
```

> **Gmail App Password:** Enable 2-Step Verification on your Google account, then generate an App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

---

## Usage

### Run the full pipeline

```bash
# From the repo root, run with PYTHONPATH pointing to src/
PYTHONPATH=src python src/main.py

# Or navigate into src/ first
cd src && python main.py
```

This will:

1. Run the **Researchers Agent** on today's trending HF papers
2. Run the **Enthusiasts Agent** on today's AI news and trending GitHub repos
3. Run the **Teachers Agent** on a fundamentals topic from Redis
4. Normalize and render all output into HTML email digests
5. Send one email per platform (LinkedIn, Instagram, Medium, YouTube) via Gmail SMTP

### Use agents individually in Python

```python
import sys
sys.path.insert(0, "src")  # ensure src is on PYTHONPATH

from agents.researchers import Researchers
from agents.teachers import Teachers
from agents.enthusiasts import Enthusiasts

researchers = Researchers()
researchers_output = researchers.run()

teachers = Teachers()
teachers_output = teachers.run()

enthusiasts = Enthusiasts()
enthusiasts_output = enthusiasts.run()
```

---

## Content Output

All output is stored under `src/assets/output/<YYYYMMDD>/`:

### `researchers.json`

```json
{
  "<paper_title>": {
    "linkedin_post":  { "hook": "...", "research_problem": "...", "key_insights": "...", "why_it_matters": "...", "closing_reflection": "...", "relavant_hashtags": "..." },
    "instagram_post": { ... },
    "medium_post":    { ... },
    "youtube_post":   { ... }
  }
}
```

### `teachers.json`

```json
{
  "linkedin_post":  { "title": "...", ... },
  "instagram_post": { "title": "...", ... },
  "medium_post":    { "title": "...", ... },
  "youtube_post":   { "title": "...", ... }
}
```

### `enthusiasts.json`

```json
{
  "news": {
    "news": {
      "linkedin_post":  { ... },
      "instagram_post": { ... },
      "youtube_video":  { ... }
    }
  },
  "repos": {
    "<repo_name>": {
      "linkedin_post":  { ... },
      "instagram_post": { ... },
      "youtube_video":  { ... }
    }
  }
}
```

### Email Distribution

The orchestrator sends four emails per run, one per platform:

| Email Subject                                      | Platform Content                    |
| -------------------------------------------------- | ----------------------------------- |
| `Your Daily AI Content on <date>: LINKEDIN POSTS`  | Professional, research-backed posts |
| `Your Daily AI Content on <date>: INSTAGRAM POSTS` | Short-form, visual-friendly content |
| `Your Daily AI Content on <date>: MEDIUM POSTS`    | Long-form technical articles        |
| `Your Daily AI Content on <date>: YOUTUBE POSTS`   | Video scripts and roundups          |

---

## Technology Stack

| Category                   | Library                  | Version       |
| -------------------------- | ------------------------ | ------------- |
| **Agent Framework**        | `langchain`              | 1.2.10        |
| **LLM — Mistral (active)** | `langchain-mistralai`    | 1.1.1         |
| **LLM — Gemini**           | `langchain-google-genai` | 3.0.1         |
| **LLM — Ollama**           | `langchain-ollama`       | 1.0.1         |
| **Tracing**                | `langsmith`              | 0.5.0         |
| **Data Validation**        | `pydantic`               | 2.12.5        |
| **PDF Processing**         | `pypdf`, `PyPDF2`        | 5.2.0 / 3.0.1 |
| **Web Scraping**           | `beautifulsoup4`         | 4.14.3        |
| **HTTP**                   | `requests`               | 2.32.3        |
| **Templating**             | `jinja2`                 | 3.1.6         |
| **Redis Client**           | `redis`                  | 7.2.0         |
| **Env Management**         | `python-dotenv`          | 1.0.1         |
| **Data**                   | `pandas`                 | 3.0.1         |
| **Progress**               | `tqdm`                   | 4.67.3        |
| **Markdown**               | `Markdown`               | 3.10          |

---

## Todos & Roadmap

See [TODO.md](TODO.md) for the full prioritized task list. Key highlights:

### 🔴 P0 — Critical (can't run / can't ship)

- Fix agent retry recursion bug (wrong method signature on retry)
- Fix `TeachersResponse` Pydantic model/schema mismatch
- Harden Redis config — avoid import-time `os.environ` failures
- Add HTTP timeouts and `raise_for_status()` to external requests

### 🟡 P1 — Important (docs / config / reproducibility)

- Standardize `PYTHONPATH` / run mode across local and CI
- Fix `.env` loading in tools (avoid CWD-dependent relative paths)
- Remove duplicate `Markdown==3.10` in `requirements.txt`
- Add Redis seeding documentation / script

### 🟢 P2–P3 — Improvements

- Add proper `pyproject.toml` and package structure
- Add unit tests for orchestrator assembly and "no content" flows
- Add `ruff` linting and `pre-commit` hooks
- Multi-platform support (Twitter/X, Bluesky, TikTok)
- Content scheduling with APScheduler or cron

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

_Built with ❤️ by [Pavan Kumar Balijepalli](https://www.linkedin.com/in/pavan-kumar-balijepalli/) · [Kundelu AI](https://youtube.com/@kundelu-ai)_
