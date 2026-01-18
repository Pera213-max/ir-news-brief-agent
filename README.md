# IR & News Brief Agent

An AI agent that generates daily company briefs by ingesting news and IR (Investor Relations) releases. Demonstrates the **Plan → Act → Reflect** agent architecture.

[![CI](https://github.com/Pera213-max/ir-news-brief-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Pera213-max/ir-news-brief-agent/actions/workflows/ci.yml)

## 🚀 Quick Start

### Option 1: Web UI (Recommended)

```bash
# Clone and install
git clone https://github.com/Pera213-max/ir-news-brief-agent.git
cd ir-news-brief-agent
pip install -e .

# Start the web interface
python -m brief_agent ui
```

Open your browser at **http://127.0.0.1:8000** and you're ready to go!

### Option 2: Command Line

```bash
python -m brief_agent run --ticker NOKIA.HE --date 2026-01-18 --mode demo
```

## 🖥️ Web UI Usage

1. **Open** http://127.0.0.1:8000 in your browser
2. **Enter** a stock ticker (e.g., `NOKIA.HE`)
3. **Select** a date
4. **Choose** a mode:
   | Mode | Description |
   |------|-------------|
   | `demo` | Works offline with sample data (no API key needed) |
   | `gemini` | Uses Google Gemini AI (requires API key) |
5. **Click** "Generate Brief"
6. **View** generated briefs in the dashboard

## ⚙️ Configuration

For AI-powered analysis, create a `.env` file:

```bash
# Copy the example
cp .env.example .env

# Add your API key (optional - demo mode works without it)
GEMINI_API_KEY=your-api-key-here
```

## 📁 Output

Generated briefs are saved to:
- `output/brief_TICKER_DATE.md` - Formatted markdown
- `output/brief_TICKER_DATE.json` - Structured JSON
- `logs/run_DATE.log` - Execution log

## What is an AI Agent?

An **AI agent** is a workflow that:
1. Takes a **goal** (e.g., "Create a brief for NOKIA.HE")
2. **Plans** steps to achieve that goal
3. **Acts** by using tools (file I/O, HTTP requests, LLM calls)
4. **Reflects** by validating output and iterating if needed

The LLM is a *component* of the agent—not the whole system.

## Features

- ✅ **Web UI** - Beautiful dashboard for easy use
- ✅ **Demo mode** - Works offline with sample data
- ✅ **Gemini AI** - Powered by Google's latest LLM
- ✅ **Plan-Act-Reflect** architecture
- ✅ **Markdown + JSON** output

## Project Structure

```
brief_agent/
├── api.py           # FastAPI web server
├── cli.py           # Command line interface
├── core.py          # Agent loop (Plan → Act → Reflect)
├── llm.py           # LLM abstraction (Demo, Gemini, etc.)
├── planner.py       # Step generation
├── tools.py         # Tool implementations
├── render.py        # Markdown rendering
└── web/             # Frontend assets
    ├── templates/   # HTML
    └── static/      # CSS, JS
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check .

# Run tests
pytest -v
```

## Roadmap

- [ ] Live RSS feed ingestion
- [ ] Embeddings-based relevance ranking
- [ ] Multi-company portfolio briefs

## License

MIT License - see [LICENSE](LICENSE)
