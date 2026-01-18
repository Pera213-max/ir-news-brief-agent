# AI Agent Instructions

These instructions are for the AI agent (and developers) implementing the IR & News Brief Agent.

## Goal
Create a robust, production-ready Python agent that produces financial briefs.

## Critical Rules
1.  **Demo Mode First**: The agent MUST work offline using `data/sample_*.json`.
2.  **No Hard Failures on Missing Keys**: If API keys are missing, silently fallback to `DemoLLM`.
3.  **Clean Output**: Ensure Markdown and JSON outputs are perfectly synced.
4.  **Git Hygiene**: Follow the branch order: `scaffold` -> `agent-loop` -> `output-render` -> `ci-and-polish`.

## Step-by-Step Implementation Guide

### Phase 1: Scaffold
1.  Initialize git repostiory.
2.  Create `pyproject.toml` with `ruff` and `pytest`.
3.  Create directory structure (`brief_agent/`, `data/`, `tests/`).
4.  Add `.gitignore` and `.env.example`.

### Phase 2: Core Logic
1.  Implement `schemas.py` to define the JSON structure.
2.  Implement `llm.py` with `DemoLLM` class.
3.  Implement `tools.py` with `read_sample_data` functions.
4.  Implement `planner.py` to return a static list of steps for now.
5.  Implement `core.py` to iterate through steps.

### Phase 3: Rendering & CLI
1.  Implement `render.py` to convert data to Markdown.
2.  Implement `cli.py` using `argparse` or `typer`.
3.  Wire everything in `__main__.py`.

### Phase 4: Quality & CI
1.  Add `tests/test_schema.py`.
2.  Add `.github/workflows/ci.yml`.
3.  Run `ruff format` and `ruff check`.
4.  Verify end-to-end run.

## Command Reference
- Run Agent: `python -m brief_agent run --ticker <TICKER> --mode demo`
- Run Tests: `pytest`
- Lint: `ruff check .`
