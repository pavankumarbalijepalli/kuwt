# Keep Up With Technology (KUWT)

## Overview

**KUWT** is an AI-powered content generation automation platform designed to keep technology enthusiasts and learners up-to-date with the latest developments in AI and technology. This project automatically generates high-quality, platform-specific educational content on technology topics for multiple channels including YouTube, LinkedIn, Instagram, and Medium.

The platform uses intelligent agents powered by LLMs (Large Language Models) to:
- Fetch and analyze trending research papers and technology news
- Generate engaging, educational content tailored to each platform's audience and format
- Maintain consistency in messaging while adapting to platform-specific requirements
- Automate the entire content creation workflow

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

- 🤖 **Multi-Agent System**: Specialized agents for different content types and platforms
- 📰 **Automated Data Collection**: Fetches latest research papers and technology news from Hugging Face and other sources
- 🎬 **Multi-Platform Content Generation**: Creates platform-optimized content for:
  - YouTube (5-minute video scripts)
  - LinkedIn (professional research posts)
  - Instagram (engaging reels)
  - Medium (in-depth articles)
- 🧠 **Flexible LLM Support**: Compatible with multiple LLM backends (Ollama, Google Gemini, and more)
- 💾 **Structured Output**: Uses Pydantic models for consistent, validated content structure
- 📊 **Content Management**: Organized storage and retrieval of generated content

## Installation

### Prerequisites

- Python 3.8+
- Git

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd air-kai-content
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your LLM backend:
   - For **Ollama**: Ensure Ollama is running locally on `localhost:11434`
   - For **Google Gemini**: Set up your API key in environment variables

## Usage

### Running the Web Interface

Start the Streamlit control panel to interact with agents:

```bash
python src/app.py
```

This opens an interactive web interface where you can:
- Select different agents (Researchers, Teachers, Enthusiasts)
- Provide input parameters
- Execute content generation workflows
- View and manage generated content

### Manual Agent Usage

You can also import and use agents directly in Python:

```python
from src.agents.researchers import Researchers
from src.brains.ollama import get_ollama_model

researchers = Researchers()
# Generate LinkedIn content on a specific topic
linkedin_content = researchers.linkedin_researcher.invoke({"topic": "transformer-models"})
```

## Project Architecture

```
air-kai-content/
├── README.md
├── requirements.txt
├── src/
│   ├── app.py                          # Streamlit web interface
│   ├── agents/                         # AI agents for content generation
│   │   ├── researchers.py              # Multi-platform research content generator
│   │   ├── teachers.py                 # Educational content specialist (TODO)
│   │   ├── enthusiasts.py              # Community-focused content (TODO)
│   │
│   ├── brains/                         # LLM backend integrations
│   │   ├── ollama.py                   # Ollama model initialization
│   │   ├── gemini.py                   # Google Gemini integration
│   │
│   ├── models/                         # Pydantic data models
│   │   ├── fundamentals.py             # YouTube/basic content models
│   │   ├── papers.py                   # Research paper content models
│   │   ├── tools_and_news.py           # Tools & news content models (TODO)
│   │
│   ├── prompts/                        # LLM system prompts
│   │   ├── fundamentals.py             # YouTube/Instagram prompts
│   │   ├── papers.py                   # LinkedIn/Medium prompts
│   │   ├── tools_and_news.py           # Tools & news prompts (TODO)
│   │
│   ├── tools/                          # Data collection utilities
│   │   ├── fetch_papers.py             # Download papers from Hugging Face
│   │   ├── fetch_tools_and_news.py     # Fetch technology news (TODO)
│   │   ├── fetch_topics.py             # Extract trending topics (TODO)
│   │
│   ├── utils/                          # Utility functions
│   │   ├── logger.py                   # Logging configuration
│   │   ├── stt.py                      # Speech-to-text utilities
│   │
│   └── assets/                         # Static files and inputs
│       └── input/fundamentals.json     # Topic/fundamental definitions
│
└── logs/                               # Application logs
```

## Agents

### 1. **Researchers Agent**
Generates research-focused, technical content optimized for different platforms:
- **LinkedIn**: Professional research posts with insights
- **Medium**: In-depth technical articles
- **YouTube**: 5-minute educational video scripts
- **Instagram**: Short, visual-friendly script snippets

### 2. **Teachers Agent** *(TODO)*
Specializes in creating educational content:
- Simplified explanations for beginners
- Progressive learning paths
- Interactive exercise suggestions
- Assessment-friendly formats

### 3. **Enthusiasts Agent** *(TODO)*
Community-focused content generation:
- Casual, engaging tone
- Discussion-starter posts
- Opinion pieces and hot takes
- Community engagement prompts

## Content Formats

Each platform has optimized content structures:

### YouTube/Fundamentals
- **Hook**: Attention-grabbing intro with real-world scenario
- **Intuition**: Simple mental model explanation
- **Technical Details**: Crisp explanations with examples
- **CTA**: Call-to-action for next topic
- **Creator Tips**: Pacing, visuals, and tone guidance

### Research Content (LinkedIn/Medium)
- **Title**: Compelling headline
- **Introduction**: Context and relevance
- **Key Findings**: Main insights from research
- **Technical Analysis**: Deep dive into methodology
- **Practical Applications**: Real-world use cases
- **Conclusion**: Takeaways and implications

## Todos & Roadmap

### High Priority
- [ ] Implement **Enthusiasts Agent** for community-focused content
- [ ] Implement **Teachers Agent** for educational content
- [ ] Complete `fetch_topics.py` tool to extract trending technology topics
- [ ] Complete `fetch_tools_and_news.py` tool for news aggregation
- [ ] Complete `tools_and_news.py` models and prompts

### Medium Priority
- [ ] Add comprehensive error handling across all agents
- [ ] Implement unit tests for all agent workflows
- [ ] Add logging to all agents for monitoring and debugging
- [ ] Create content review/approval workflow
- [ ] Add content scheduling and publishing automation

### Low Priority
- [ ] Support for additional platforms (TikTok, Twitter/X, Reddit)
- [ ] Multi-language content generation
- [ ] Advanced content personalization
- [ ] Analytics dashboard for content performance
- [ ] Integration with third-party publishing platforms

### Code Improvements
- [ ] Add comprehensive docstrings to all modules
- [ ] Implement configuration management (config.yaml)
- [ ] Add dependency injection for LLM backends
- [ ] Implement caching for frequently generated content
- [ ] Create comprehensive API documentation

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
