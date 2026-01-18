# Project: IR & News Brief Agent (public, runnable, recruiter-friendly)
Build a Python-based AI agent that generates a daily company brief (MD + JSON)
by ingesting news + IR releases (demo mode uses sample data).
This is a practical example aligned with SaaS product work and automation.

## Repo
- Name: ir-news-brief-agent
- Visibility: Public
- Default branch: main

## Definition of Done (Phase 1)
1) Running this command works in demo mode (no network, no API keys):
   python -m brief_agent run --ticker NOKIA.HE --date 2026-01-18 --mode demo

2) Outputs are created:
   - output/brief_NOKIA.HE_2026-01-18.md
   - output/brief_NOKIA.HE_2026-01-18.json
   - logs/run_2026-01-18.log

3) Agent architecture demonstrates plan -> act -> reflect.
4) No secrets committed. .env ignored. .env.example included.
5) Minimal quality gates: ruff + pytest + GitHub Actions CI.
6) Clean git history with 8–15 meaningful commits.
7) Use feature branches and at least one PR merge (even if solo).

---

# Core Concept (must be in README)
Explain succinctly:
- An AI agent is a workflow that takes a goal, plans steps, uses tools (IO/HTTP),
  and verifies output. The LLM is a component (demo or API), not the whole system.

---

# Data Sources (Phase 1)
## Demo mode (required)
Use local sample files under /data:
- data/sample_news.json
- data/sample_ir.json

No internet required.

## Optional live mode (Phase 1.5)
- RSS feeds and/or yfinance/news APIs if keys exist
- If keys missing, automatically fallback to demo mode.
Never block execution due to missing keys.

---

# Output Requirements
## Markdown brief must include these sections
- Summary (3–6 bullets)
- Company snapshot (ticker, date, quick metrics if available)
- IR releases (top 3 items)
- News highlights (top 5 items)
- Key drivers & risks (LLM-generated but grounded in provided items)
- Notes & limitations (disclaimer)

## JSON schema (must match MD content)
{
  "date": "YYYY-MM-DD",
  "ticker": "NOKIA.HE",
  "summary_bullets": ["..."],
  "ir_releases": [{"title":"", "date":"", "source":"", "url":""}],
  "news": [{"title":"", "source":"", "url":""}],
  "drivers": ["..."],
  "risks": ["..."],
  "limitations": ["..."]
}

---

# Architecture & File Tree (must implement)
/brief_agent
  __init__.py
  __main__.py            # allows: python -m brief_agent ...
  cli.py                 # argparse/typer entry
  core.py                # orchestrates plan/act/reflect
  planner.py             # produces ordered steps
  tools.py               # tool interface + implementations
  llm.py                 # LLM abstraction: DemoLLM + optional API LLM
  cache.py               # file-based cache
  render.py              # markdown rendering
  schemas.py             # pydantic models for JSON output
  utils.py               # logging, helpers

/data
  sample_news.json
  sample_ir.json

/docs
  ARCHITECTURE.md
  EXAMPLE_OUTPUT.md
  images/ (optional screenshots)

/output               # gitignored
/logs                 # gitignored

.github/workflows/ci.yml

README.md
pyproject.toml
.env.example
.gitignore
LICENSE

---

# LLM Handling (important)
Implement llm.py with a simple interface:
- DemoLLM: deterministic templated outputs; no API calls.
- Optional: Anthropic/OpenAI LLM if env vars exist.
  - Read keys from env only: ANTHROPIC_API_KEY / OPENAI_API_KEY
  - If missing, fallback to DemoLLM without error.

The agent MUST be runnable with DemoLLM by default.

---

# Planner + Tooling spec
## Planner steps (example)
Given goal: "Create brief for TICKER on DATE"
Planner returns steps:
1) Load IR items (demo: from file)
2) Load news items (demo: from file)
3) Select top items (simple heuristics)
4) Ask LLM to draft summary/drivers/risks from the selected items
5) Render markdown
6) Validate that all required sections exist
7) Save MD + JSON

## Tools
Implement tools with explicit names:
- read_sample_ir(ticker, date) -> list
- read_sample_news(ticker, date) -> list
- select_top_items(items, n, rules) -> list
- llm_generate_sections(context) -> dict
- write_output_files(md, json, paths) -> None

## Reflection / validation
Validate:
- MD contains required headings
- JSON matches schema
If missing: do one revision attempt (e.g., regenerate sections) then fail with
actionable error message.

---

# Quickstart
Must support:
pip install -r requirements (or pip install -e .)
python -m brief_agent run --ticker NOKIA.HE --date 2026-01-18 --mode demo

---

# Quality
## pyproject.toml
- ruff (lint + format)
- pytest

## tests/
- test_schema.py: validates JSON output schema
- test_select_top.py: validates selection logic

## CI workflow (GitHub Actions)
- install
- ruff check
- pytest

---

# Security & Hygiene
- Add .gitignore:
  .env, .env.*, output/, logs/, __pycache__/, .venv/, .pytest_cache/
- Add .env.example with placeholders (no real keys).
- Ensure sample data contains no personal/private data.

---

# Git workflow instructions (the agent MUST follow)
## Auth note
You (the agent) will commit and push using my local git credentials
or via GitHub CLI (gh). Make git stuff and more for security. 

## Branch plan and pushing sequence
1) Start from main:
   git checkout main
   git pull origin main

2) Create branches in this order and push each:
   a) feature/scaffold
   b) feature/agent-loop
   c) feature/output-render
   d) feature/ci-and-polish

3) For each branch:
   - make small coherent changes
   - run basic checks locally
   - commit with conventional messages
   - push branch

Commit message style (examples):
- chore: add project scaffold and gitignore
- docs: add README and architecture overview
- feat: implement plan-act-reflect core loop
- feat: add demo data tools and selection logic
- feat: render markdown + json output
- test: add schema and selection unit tests
- ci: add GitHub Actions workflow
- refactor: simplify tool interfaces

## Pull Requests (must do at least one)
After pushing each branch, create PR and merge:
- Use GitHub CLI if available:
  gh pr create --fill
  gh pr merge --merge --delete-branch

If GH CLI is not available, instruct the user to open PR in UI, but still push
branches in correct order.

## Post-merge
- Pull latest main
- Tag a release (optional): v0.1.0

---

# Deliverables you must produce at the end
1) Full working repo with the tree above.
2) Example output files committed under /docs (NOT /output).
3) README that explains:
   - what an agent is
   - how this relates to real product work
   - how to run demo mode in 60 seconds
4) A short Roadmap section (Phase 2 ideas):
   - live RSS ingestion
   - embeddings-based relevance ranking
   - TradeMaster integration endpoint
