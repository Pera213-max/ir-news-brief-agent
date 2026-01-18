"""FastAPI backend for IR & News Brief Agent."""

import json
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .core import Agent
from .utils import get_logger

# Initialize app
app = FastAPI(title="IR & News Brief Agent API")
logger = get_logger()

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR.parent / "output"
WEB_DIR = BASE_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class GenerateRequest(BaseModel):
    ticker: str
    date: str
    mode: str = "demo"


def run_agent_task(ticker: str, date: str, mode: str):
    """Background task to run the agent."""
    try:
        logger.info(f"Starting background generation for {ticker} on {date}")
        agent = Agent(mode=mode)
        agent.run(ticker=ticker, date=date)
        logger.info("Background generation completed")
    except Exception as e:
        logger.error(f"Background generation failed: {e}")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main dashboard."""
    index_path = TEMPLATES_DIR / "index.html"
    return FileResponse(index_path)


@app.get("/api/briefs")
async def list_briefs():
    """List all generated brief files."""
    if not OUTPUT_DIR.exists():
        return []

    briefs = []
    # List JSON files as they are easier to parse metadata from filename if needed
    # Naming convention: brief_TICKER_DATE.json
    for file in OUTPUT_DIR.glob("*.json"):
        try:
            parts = file.stem.split("_")
            if len(parts) >= 3:
                ticker = parts[1]
                date = parts[2]
                briefs.append(
                    {
                        "filename": file.name,
                        "ticker": ticker,
                        "date": date,
                        "timestamp": file.stat().st_mtime,
                    }
                )
        except Exception:
            continue

    # Sort by date (newest first)
    return sorted(briefs, key=lambda x: x["timestamp"], reverse=True)


@app.get("/api/briefs/{filename}")
async def get_brief_content(filename: str):
    """Get the content of a specific brief."""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Brief not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            if filename.endswith(".json"):
                return json.load(f)
            else:
                return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate")
async def generate_brief(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Trigger brief generation."""
    background_tasks.add_task(run_agent_task, request.ticker, request.date, request.mode)
    return {"status": "accepted", "message": f"Generation started for {request.ticker}"}
