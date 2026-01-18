# Architecture Overview

This document describes the architecture of the IR & News Brief Agent.

## Core Concept: Plan → Act → Reflect

```
┌──────────────────────────────────────────────────────────────┐
│                          AGENT                               │
│  ┌─────────┐    ┌─────────┐    ┌───────────┐               │
│  │  PLAN   │───▶│   ACT   │───▶│  REFLECT  │               │
│  │         │    │         │    │           │               │
│  │ Planner │    │  Tools  │    │ Validator │               │
│  └─────────┘    └─────────┘    └───────────┘               │
│       │              │               │                       │
│       ▼              ▼               ▼                       │
│   Steps List    Context Data    Validation                  │
└──────────────────────────────────────────────────────────────┘
```

## Components

### 1. Core (`core.py`)
The main `Agent` class orchestrates the entire workflow:
- Initializes context and dependencies
- Executes the plan-act-reflect loop
- Handles errors and recovery

### 2. Planner (`planner.py`)
Generates an ordered list of execution steps:
1. Load IR releases
2. Load news items
3. Select top items
4. Generate LLM sections
5. Render output
6. Validate
7. Save files

### 3. Tools (`tools.py`)
Implements discrete operations:
- `read_sample_ir()` - Load IR data
- `read_sample_news()` - Load news data
- `select_top_items()` - Filter and sort
- `llm_generate_sections()` - LLM inference
- `write_output_files()` - File I/O
- `validate_output()` - Schema validation

### 4. LLM (`llm.py`)
Abstraction layer with fallback:,
```
DemoLLM (default) ─┬─▶ OpenAI LLM (if key exists)
                   └─▶ Anthropic LLM (if key exists)
```

### 5. Schemas (`schemas.py`)
Pydantic models ensure type safety:
- `IRRelease` - IR announcement
- `NewsItem` - News article
- `BriefOutput` - Complete brief

## Data Flow

```
Input: (ticker, date)
         │
         ▼
┌─────────────────┐
│   Load Data     │ ──▶ sample_ir.json, sample_news.json
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Select Top N   │ ──▶ 3 IR releases, 5 news items
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  LLM Generate   │ ──▶ Summary, Drivers, Risks
└─────────────────┘
         │
         ▼
┌─────────────────┐
│     Render      │ ──▶ Markdown + JSON
└─────────────────┘
         │
         ▼
Output: brief_TICKER_DATE.md, brief_TICKER_DATE.json
```

## Extension Points

1. **New Data Sources**: Add functions in `tools.py` for RSS, APIs
2. **New LLM Providers**: Extend `BaseLLM` in `llm.py`
3. **Output Formats**: Add renderers in `render.py`
