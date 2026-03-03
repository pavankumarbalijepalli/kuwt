# Keep Up With Technology (KUWT)

## Overview

**KUWT** is an AI-powered content generation automation platform designed to keep technology enthusiasts and learners up-to-date with the latest developments in AI and technology. This project automatically generates high-quality, platform-specific educational content on technology topics for multiple channels including YouTube, LinkedIn, Instagram, and Medium.

The platform uses intelligent agents powered by LLMs (Large Language Models) to:

- Fetch and analyze trending research papers, technology news, and GitHub repositories
- Generate engaging, educational content tailored to each platform's audience and format
- Maintain consistency in messaging while adapting to platform-specific requirements
- Automate the entire content creation workflow with orchestrated agent coordination
- Distribute content via automated email notifications

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Architecture](#project-architecture)
- [Agents](#agents)
- [Content Formats](#content-formats)
- [Todos & Roadmap](#todos--roadmap)
- [Contributing](#contributing)

## Features

- 🤖 **Three Specialized Agents**: Researchers, Teachers, and Enthusiasts agents for different content types
- 📰 **Automated Data Collection**:
  - Fetches trending research papers from Hugging Face
  - Aggregates technology news and AI developments
  - Discovers trending GitHub repositories
- 🎬 **Multi-Platform Content Generation**: Creates platform-optimized content for:
  - **LinkedIn** - Professional, research-backed posts
  - **Medium** - In-depth technical articles
  - **Instagram** - Engaging, visual-friendly content
  - **YouTube** - 5-minute educational video scripts
- 🧠 **Flexible LLM Support**: Compatible with multiple LLM backends (Google Gemini, Ollama, OpenAI)
- 💾 **Structured Output**: Uses Pydantic models for consistent, validated content structure
- 📧 **Automated Email Distribution**: Sends platform-specific content emails for easy publishing
- 🎛️ **Dual Interface**: Web UI for interactive use or CLI for automation/scheduling
- 📊 **Organized Content Management**: Structured storage organized by date and content type

## Installation

### Prerequisites

- Python 3.11+

- Git
- Google Gemini API key (for LLM functionality)
- SMTP email credentials (for email distribution)
- Internet connection (for paper fetching and API calls)

### Quick Start

1. Clone the repository:

```bash
git clone <repository-url>
cd air-kuwt
```

1. Create a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Configure environment variables:

Create a `.env` file in the project root with the following variables:

```bash
# Google Gemini API Configuration
RESEARCHER_GEMINI=<your-gemini-api-key>
TEACHER_GEMINI=<your-gemini-api-key>
ENTHUSIAST_GEMINI=<your-gemini-api-key>

# Email Configuration (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=<your-email@gmail.com>
SENDER_PASSWORD=<your-app-password>
RECIPIENT_EMAIL=<recipient-email@example.com>

# Optional: Ollama Configuration (if using local models)
OLLAMA_BASE_URL=http://localhost:11434
```

1. Prepare input data:

- Create `src/assets/input/fundamentals.json` with topic definitions
- Create `src/assets/input/covered.json` to track covered content (optional)

## Usage

### Running the Full Automation Pipeline

Execute the complete workflow with agent orchestration and email distribution:

```bash
python src/main.py
```

This will:

1. Run the **Researchers Agent** to generate research paper content
2. Run the **Teachers Agent** to generate educational content
3. Run the **Enthusiasts Agent** to generate news and trending repository content
4. Aggregate all content by platform (LinkedIn, Instagram, Medium, YouTube)
5. Send platform-specific content via email for review and publishing

### Running the Web Interface

Start the interactive Streamlit control panel to interact with agents individually:

```bash
streamlit run src/app.py
```

This opens a web interface where you can:

- Select specific agents (Researchers, Teachers, or Enthusiasts)
- Configure content parameters
- Execute individual agent workflows
- View generated content in real-time
- Download and manage output files

### Manual Agent Usage

You can also import and use agents directly in Python scripts:

```python
from agents.researchers import Researchers
from agents.teachers import Teachers
from agents.enthusiasts import Enthusiasts

# Initialize agents
researchers = Researchers()
teachers = Teachers()
enthusiasts = Enthusiasts()

# Run individual agents
researchers.run()
teachers.run()
enthusiasts.run()
```

## Project Architecture

```text
air-kuwt/
├── README.md
├── requirements.txt
├── src/
│   ├── app.py                          # Streamlit web interface
│   ├── main.py                         # Agent orchestrator and email automation
│   ├── agents/                         # AI agent implementations
│   │   ├── researchers.py              # Research paper content generator
│   │   ├── teachers.py                 # Educational fundamentals content generator
│   │   └── enthusiasts.py              # Technology news & repos content generator
│   │
│   ├── brains/                         # LLM backend integrations
│   │   ├── gemini.py                   # Google Gemini integration
│   │   ├── github_openai.py            # GitHub OpenAI integration
│   │   └── ollama.py                   # Ollama local model integration
│   │
│   ├── models/                         # Pydantic data models
│   │   ├── fundamentals.py             # Educational content models
│   │   ├── papers.py                   # Research paper content models
│   │   └── tools_and_news.py           # News & repository content models
│   │
│   ├── prompts/                        # LLM system prompts
│   │   ├── fundamentals.py             # Educational content prompts
│   │   ├── papers.py                   # Research content prompts
│   │   └── tools_and_news.py           # News & repository prompts
│   │
│   ├── tools/                          # Data collection utilities
│   │   ├── fetch_papers.py             # Download papers from Hugging Face
│   │   ├── fetch_tools_and_news.py     # Fetch technology news and repos
│   │   └── fetch_topics.py             # Extract trending topics
│   │
│   ├── utils/                          # Utility functions
│   │   ├── logger.py                   # Logging configuration
│   │   ├── email_handler.py            # SMTP email utilities
│   │   ├── stt.py                      # Speech-to-text utilities
│   │   └── json_tree.py                # JSON processing utilities
│   │
│   └── assets/                         # Static files and content storage
│       ├── input/                      # Input data sources
│       │   ├── fundamentals.json       # Topic/fundamental definitions
│       │   ├── covered.json            # Previously covered content tracking
│       │   └── papers/                 # Downloaded research papers (by date)
│       └── output/                     # Generated content by date
│
└── logs/                               # Application logs
```

## Agents

The system uses three specialized agents that work together to create comprehensive technology content:

### 1. **Researchers Agent**

Analyzes academic research papers and generates technical, research-focused content:

- **Input**: Trending research papers from Hugging Face and academic sources
- **Output Formats**:
  - **LinkedIn**: Professional research posts with key findings and implications
  - **Medium**: In-depth technical articles with methodology and analysis
  - **YouTube**: 5-minute educational video scripts with visual cues
  - **Instagram**: Short, visual-friendly script snippets with key takeaways

### 2. **Teachers Agent**

Creates educational content focused on fundamental concepts and learning:

- **Input**: Core AI/technology fundamentals and topics
- **Output Formats**:
  - **LinkedIn**: Professional educational posts with progressive learning paths
  - **Medium**: Tutorial articles with examples and best practices
  - **YouTube**: Educational explainer scripts with clear progression
  - **Instagram**: Bite-sized learning tips and concept visualizations

### 3. **Enthusiasts Agent**

Generates community-focused content from technology news and trending repositories:

- **Input**: Technology news, GitHub trending repositories, and community discussions
- **Output Formats**:
  - **LinkedIn**: Engaging posts about trending tools and news
  - **Medium**: Opinion pieces and trend analysis articles
  - **YouTube**: News roundup scripts and community highlight videos
  - **Instagram**: Trending tool announcements and community highlights

## Agent Orchestrator

The `AgentOrchestrator` in [src/main.py](src/main.py) coordinates all three agents:

- Executes agents sequentially to generate daily content
- Aggregates output from all agents into platform-specific formats
- Prepares email notifications with generated content
- Distributes content via SMTP email for manual publishing or automation

## Content Formats

Each agent produces structured JSON output containing content for all platforms. The output is organized by date in the `src/assets/output/` directory:

### Researchers Agent Output (`researchers.json`)

```json
{
  "paper_title": {
    "linkedin_post": { "title": "...", "content": "..." },
    "instagram_post": { "title": "...", "content": "..." },
    "medium_post": { "title": "...", "content": "..." },
    "youtube_post": { "title": "...", "content": "..." }
  }
}
```

### Teachers Agent Output (`teachers.json`)

```json
{
  "topic_name": {
    "linkedin": "...",
    "instagram": "...",
    "medium": "...",
    "youtube": "..."
  }
}
```

### Enthusiasts Agent Output (`enthusiasts.json`)

```json
{
  "news": {
    "news": {
      "linkedin": "...",
      "instagram": "...",
      "medium": "...",
      "youtube": "..."
    }
  },
  "repos": {
    "repo_name": {
      "linkedin": "...",
      "instagram": "...",
      "medium": "...",
      "youtube": "..."
    }
  }
}
```

### Email Distribution

The orchestrator aggregates content from all three agents into four platform-specific emails:

1. **LinkedIn Posts** - Professional, research-focused content
2. **Instagram Posts** - Visual, engaging, short-form content
3. **Medium Posts** - In-depth, long-form articles
4. **YouTube Posts** - Script content for video creation

## Todos & Roadmap

### High Priority

- Enhance content quality validation and review workflow
- Implement comprehensive error handling and retry logic for API failures
- Add scheduling system for daily automated runs (cron/APScheduler)
- Create content tracking system to avoid duplicates and repetition
- Improve email templates with better formatting and branding

### Medium Priority

- Add unit tests for all agent workflows
- Implement detailed logging and monitoring for production deployment
- Create dashboard for content performance analytics
- Add content review/approval workflow before email distribution
- Implement content caching to reduce API calls
- Support for additional LLM backends (OpenAI, Claude, etc.)

### Low Priority

- Support for additional platforms (TikTok, Twitter/X, Bluesky, Reddit)
- Multi-language content generation
- Advanced content personalization by audience segment
- Integration with third-party publishing platforms (Buffer, Hootsuite)
- ML-based optimal posting time calculation
- Advanced analytics for engagement metrics

### Code Quality

- Add comprehensive docstrings to all modules
- Implement configuration management system (config.yaml/environment variables)
- Add dependency injection for cleaner LLM backend integration
- Create comprehensive API/module documentation
- Refactor email handling for better template management
- Add type hints throughout codebase

## Technology Stack

### Core Dependencies

- **LangChain** (`langchain-core`, `langchain-ollama`, `langsmith`) - Agent and LLM orchestration framework
- **Pydantic** - Data validation and structured output with `response_format`
- **Hugging Face Hub** - Access to research papers and model cards
- **Google Gemini API** - Primary LLM backend for agent reasoning
- **PDF Processing** (`pypdf`, `PyPDF2`) - Extract text from research papers

### Content Generation & Audio

- **Transformers** - NLP models for embeddings and analysis
- **TorchData/TorchTune** - PyTorch utilities for efficient data handling
- **Kokoro** - AI voice synthesis for potential audio content
- **SoundFile** - Audio file I/O utilities

### Integration & Communication

- **Requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **secure-smtplib** - Secure email distribution

### Development

- **Markdown** - Processing markdown formatted content
- **LangSmith** - Debugging and monitoring for LangChain workflows

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
