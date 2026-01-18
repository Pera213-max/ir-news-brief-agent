# IR & News Brief Agent

An AI agent that generates daily company briefs by ingesting news and IR (Investor Relations) releases. Demonstrates the **Plan → Act → Reflect** agent architecture.

[![CI](https://github.com/YOUR_USERNAME/ir-news-brief-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/ir-news-brief-agent/actions/workflows/ci.yml)

## What is an AI Agent?

An **AI agent** is a workflow that:
1. Takes a **goal** (e.g., "Create a brief for NOKIA.HE")
2. **Plans** steps to achieve that goal
3. **Acts** by using tools (file I/O, HTTP requests, LLM calls)
4. **Reflects** by validating output and iterating if needed

The LLM is a *component* of the agent—not the whole system. The agent orchestrates data flow, tool usage, and error handling.

## Quick Start (60 seconds)

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/ir-news-brief-agent.git
cd ir-news-brief-agent
pip install -e .

# Run in demo mode (no API keys needed)
python -m brief_agent run --ticker NOKIA.HE --date 2026-01-18 --mode demo
```

**Output:**
- `output/brief_NOKIA.HE_2026-01-18.md` - Formatted markdown brief
- `output/brief_NOKIA.HE_2026-01-18.json` - Structured JSON data
- `logs/run_2026-01-18.log` - Execution log

## Features

- ✅ **Demo mode** - Works offline with sample data
- ✅ **Plan-Act-Reflect** architecture
- ✅ **Markdown + JSON** output
- ✅ **Extensible LLM support** (OpenAI, Anthropic when keys provided)
- ✅ **File-based caching**
- ✅ **Comprehensive logging**

## Project Structure

```
brief_agent/
├── __init__.py      # Package init
├── __main__.py      # Entry point
├── cli.py           # CLI argument parsing
├── core.py          # Agent loop (Plan → Act → Reflect)
├── planner.py       # Step generation
├── tools.py         # Tool implementations
├── llm.py           # LLM abstraction
├── render.py        # Markdown rendering
├── schemas.py       # Pydantic models
├── cache.py         # File-based caching
└── utils.py         # Logging & helpers
```

## How It Relates to Product Work

This project demonstrates skills directly applicable to SaaS product development:

| This Project | Real-World Application |
|--------------|------------------------|
| Agent orchestration | Workflow automation, background jobs |
| LLM integration | AI features, content generation |
| Structured output | API response formatting |
| Data validation | Input/output contracts |
| CLI tooling | Developer experience |

## Configuration

Copy `.env.example` to `.env` and optionally add API keys:

```bash
# Optional - enables live LLM mode
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Logging level
LOG_LEVEL=INFO
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check .
ruff format .

# Run tests
pytest -v
```

## Roadmap (Phase 2)

- [ ] Live RSS feed ingestion
- [ ] Embeddings-based relevance ranking
- [ ] TradeMaster integration endpoint
- [ ] Historical brief comparison
- [ ] Multi-company portfolio briefs

## License

MIT License - see [LICENSE](LICENSE)
