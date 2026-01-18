"""Tool implementations for the agent."""

import json
from pathlib import Path
from typing import Any

from .llm import BaseLLM
from .schemas import BriefOutput
from .utils import ensure_directory, get_logger

# Base path for data files
DATA_DIR = Path(__file__).parent.parent / "data"


def read_sample_ir(ticker: str, date: str) -> list[dict[str, Any]]:
    """
    Read sample IR releases from local file.

    Args:
        ticker: Stock ticker (used for filtering in live mode)
        date: Date string (used for filtering in live mode)

    Returns:
        List of IR release dictionaries
    """
    logger = get_logger()
    ir_file = DATA_DIR / "sample_ir.json"

    if not ir_file.exists():
        logger.warning(f"Sample IR file not found: {ir_file}")
        return []

    try:
        with open(ir_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} IR releases from sample data")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse IR data: {e}")
        return []


def read_sample_news(ticker: str, date: str) -> list[dict[str, Any]]:
    """
    Read sample news items from local file.

    Args:
        ticker: Stock ticker (used for filtering in live mode)
        date: Date string (used for filtering in live mode)

    Returns:
        List of news item dictionaries
    """
    logger = get_logger()
    news_file = DATA_DIR / "sample_news.json"

    if not news_file.exists():
        logger.warning(f"Sample news file not found: {news_file}")
        return []

    try:
        with open(news_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} news items from sample data")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse news data: {e}")
        return []


def select_top_items(
    items: list[dict[str, Any]], n: int = 5, sort_by: str = "date"
) -> list[dict[str, Any]]:
    """
    Select top N items based on sorting criteria.

    Args:
        items: List of items to select from
        n: Number of items to return
        sort_by: Field to sort by (default: "date")

    Returns:
        Top N items sorted by the specified field
    """
    logger = get_logger()

    if not items:
        return []

    # Sort by date (most recent first) if available
    try:
        sorted_items = sorted(items, key=lambda x: x.get(sort_by, ""), reverse=True)
    except TypeError:
        # If sorting fails, return items as-is
        sorted_items = items

    result = sorted_items[:n]
    logger.info(f"Selected top {len(result)} items from {len(items)} total")
    return result


def llm_generate_sections(llm: BaseLLM, context: dict[str, Any]) -> dict[str, Any]:
    """
    Use LLM to generate brief sections.

    Args:
        llm: LLM instance to use for generation
        context: Context containing ticker, ir_releases, news items

    Returns:
        Dictionary with summary_bullets, drivers, risks, limitations
    """
    logger = get_logger()
    logger.info("Generating sections via LLM")

    result = llm.generate_sections(context)
    logger.info(f"Generated {len(result.get('summary_bullets', []))} summary bullets")
    return result


def write_output_files(
    brief: BriefOutput, output_dir: Path | str = "output"
) -> tuple[Path, Path]:
    """
    Write brief to markdown and JSON files.

    Args:
        brief: Validated brief output
        output_dir: Directory to write files to

    Returns:
        Tuple of (markdown_path, json_path)
    """
    from .render import render_markdown

    logger = get_logger()
    output_dir = ensure_directory(output_dir)

    # Generate filenames
    base_name = f"brief_{brief.ticker}_{brief.date}"
    md_path = output_dir / f"{base_name}.md"
    json_path = output_dir / f"{base_name}.json"

    # Write markdown
    md_content = render_markdown(brief)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    logger.info(f"Wrote markdown brief to {md_path}")

    # Write JSON
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(brief.model_dump_json(indent=2))
    logger.info(f"Wrote JSON brief to {json_path}")

    return md_path, json_path


def validate_output(brief: BriefOutput) -> list[str]:
    """
    Validate that the brief contains all required sections.

    Args:
        brief: Brief to validate

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Check summary bullets
    if len(brief.summary_bullets) < 3:
        errors.append("Summary should have at least 3 bullets")
    if len(brief.summary_bullets) > 6:
        errors.append("Summary should have at most 6 bullets")

    # Check IR releases
    if not brief.ir_releases:
        errors.append("At least one IR release is required")

    # Check news
    if not brief.news:
        errors.append("At least one news item is required")

    # Check drivers and risks
    if not brief.drivers:
        errors.append("At least one driver is required")
    if not brief.risks:
        errors.append("At least one risk is required")

    return errors
