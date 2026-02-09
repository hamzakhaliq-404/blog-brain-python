# Blog Brain - AI Content Generation System

[![GitHub](https://img.shields.io/badge/GitHub-blog--brain--python-blue?logo=github)](https://github.com/hamzakhaliq-404/blog-brain-python)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.108%2B-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange)](https://www.crewai.com/)

An autonomous multi-agent system that generates SEO-optimized, publication-ready blog posts using CrewAI and Google Gemini.

## 🔗 Repository

**GitHub**: [github.com/hamzakhaliq-404/blog-brain-python](https://github.com/hamzakhaliq-404/blog-brain-python)

## Overview

Blog Brain is a headless Python backend that functions as an autonomous editorial team. It accepts a topic as input and outputs fully formatted, SEO-optimized, production-ready blog content without human intervention.

### Key Features

- 🤖 **Multi-Agent Architecture**: 4 specialized AI agents working together
- 🔍 **Autonomous Research**: Automatic Google search and web scraping
- 📈 **SEO Optimization**: Built-in SEO strategy and keyword optimization
- ✍️ **Human-like Writing**: Natural, engaging content
- 🚀 **REST API**: Easy integration with any frontend

### The Team

1. **Senior Research Analyst** - Deep dive research and data gathering
2. **SEO Strategist** - Content architecture and optimization
3. **Lead Writer** - Creative, engaging content creation
4. **Managing Editor** - Quality assurance and final formatting

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Serper.dev API key ([Get one here](https://serper.dev))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hamzakhaliq-404/blog-brain-python.git
   cd blog-brain-python
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key
   SERPER_API_KEY=your_actual_serper_api_key
   ```

4. **Run the server**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Usage

### Generate Content

**Endpoint:** `POST /api/v1/generate-post`

**Request:**
```json
{
  "topic": "The Future of AI in Healthcare",
  "target_audience": "Medical Professionals",
  "tone": "professional but optimistic",
  "exclude_keywords": ["ChatGPT", "Robots"]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "meta_data": {
      "seo_title": "AI in Healthcare: 5 Trends for 2026",
      "meta_description": "Discover how AI is transforming healthcare...",
      "slug": "ai-healthcare-trends-2026",
      "focus_keyword": "AI in Healthcare"
    },
    "content": {
      "html_body": "<h2>Introduction</h2><p>...</p>",
      "markdown_body": "## Introduction\n...",
      "estimated_read_time": "5 mins"
    },
    "sources": [
      "https://example.com/source-1",
      "https://example.com/source-2"
    ],
    "word_count": 1850
  }
}
```

### Health Check

**Endpoint:** `GET /health`

Returns the API health status.

## Project Structure

```
blog-brain-python/
├── main.py                 # FastAPI server entry point
├── crew.py                 # CrewAI orchestration logic
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example            # Environment template
│
├── agents/                 # AI agent definitions
│   ├── researcher.py
│   ├── strategist.py
│   ├── writer.py
│   └── editor.py
│
├── tasks/                  # Task specifications
│   ├── research_task.py
│   ├── strategy_task.py
│   ├── writing_task.py
│   └── editing_task.py
│
├── tools/                  # Custom tools
│   ├── search_tools.py
│   └── scraper_tools.py
│
├── schemas/                # Pydantic models
│   ├── request_schema.py
│   └── response_schema.py
│
├── utils/                  # Utilities
│   ├── logger.py
│   └── helpers.py
│
└── tests/                  # Test suite
    ├── test_agents.py
    ├── test_tools.py
    └── test_api.py
```

## Configuration

All configuration is managed through environment variables in the `.env` file:

- **API Keys**: Gemini and Serper API credentials
- **Server Settings**: Host, port, reload options
- **Agent Parameters**: Temperature settings for each agent
- **CrewAI Options**: Memory, delegation, iterations

See `.env.example` for all available options.

## Technology Stack

- **Language**: Python 3.11+
- **Agent Framework**: CrewAI
- **LLM**: Google Gemini 1.5 Pro
- **API Framework**: FastAPI
- **Search**: Serper.dev API
- **Web Scraping**: BeautifulSoup4

## Cost Estimates

### Per Article
- Gemini API: ~$0.28
- Serper searches: ~$0.50
- **Total: ~$0.78 per article**

### Monthly (100 articles)
- API costs: ~$28
- Hosting: ~$25-40
- **Total: ~$53-68/month**

Compare this to $50-150 per article for human writers (95%+ cost savings).

## Development Status

This project is currently in active development. See the implementation plan for the full development roadmap.

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. tests/
```

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

---

**Built with ❤️ using CrewAI and Google Gemini**
