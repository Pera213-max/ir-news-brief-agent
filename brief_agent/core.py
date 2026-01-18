"""Core agent loop implementing Plan -> Act -> Reflect."""

from pathlib import Path
from typing import Any

from .llm import get_llm
from .planner import Planner, StepType
from .schemas import BriefOutput, IRRelease, NewsItem
from .tools import (
    fetch_live_ir,
    fetch_live_news,
    fetch_live_stock_info,
    llm_generate_sections,
    read_sample_ir,
    read_sample_news,
    select_top_items,
    validate_output,
    write_output_files,
)
from .utils import setup_logging


class Agent:
    """
    The main agent that orchestrates the Plan -> Act -> Reflect loop.
    """

    def __init__(self, mode: str = "demo"):
        """
        Initialize the agent.

        Args:
            mode: LLM mode ("demo", "openai", "anthropic")
        """
        self.logger = setup_logging()
        self.planner = Planner()
        self.llm = get_llm(mode)
        self.mode = mode

        # Context to store intermediate results
        self.context: dict[str, Any] = {}

    def run(self, ticker: str, date: str) -> tuple[Path, Path] | None:
        """
        Run the agent to generate a brief.

        Args:
            ticker: Stock ticker symbol
            date: Date for the brief (YYYY-MM-DD)

        Returns:
            Tuple of (markdown_path, json_path) if successful, None otherwise
        """
        self.logger.info("=== Starting Agent Run ===")
        self.logger.info(f"Ticker: {ticker}, Date: {date}, Mode: {self.mode}")

        # Initialize context
        self.context = {
            "ticker": ticker,
            "date": date,
            "mode": self.mode,
            "ir_releases_raw": [],
            "news_raw": [],
            "ir_releases": [],
            "news": [],
            "generated_sections": {},
            "brief": None,
        }

        # PLAN phase
        self.logger.info("--- PLAN Phase ---")
        goal = {"ticker": ticker, "date": date, "mode": self.mode}
        steps = self.planner.plan(goal)

        # ACT phase
        self.logger.info("--- ACT Phase ---")
        for i, step in enumerate(steps, 1):
            self.logger.info(f"Executing step {i}/{len(steps)}: {step}")

            try:
                self._execute_step(step)
            except Exception as e:
                self.logger.error(f"Step failed: {e}")
                # REFLECT: Try once more for generation steps
                if step.step_type == StepType.GENERATE_SECTIONS:
                    self.logger.info("Attempting recovery...")
                    try:
                        self._execute_step(step)
                    except Exception as retry_e:
                        self.logger.error(f"Recovery failed: {retry_e}")
                        return None
                else:
                    return None

        # REFLECT phase
        self.logger.info("--- REFLECT Phase ---")
        brief = self.context.get("brief")
        if not brief:
            self.logger.error("No brief was generated")
            return None

        errors = validate_output(brief)
        if errors:
            self.logger.warning(f"Validation issues: {errors}")
            # Non-fatal for now, but logged

        result = self.context.get("output_paths")
        if result:
            self.logger.info("=== Agent Run Complete ===")
            self.logger.info(f"Output: {result[0]}")
            return result

        return None

    def _execute_step(self, step) -> None:
        """Execute a single plan step."""
        # Use live data for all modes except demo
        use_live_data = self.mode != "demo"

        match step.step_type:
            case StepType.LOAD_IR:
                if use_live_data:
                    # Fetch live IR data
                    stock_info = self.context.get("stock_info", {})
                    company_name = stock_info.get("name", "")
                    self.context["ir_releases_raw"] = fetch_live_ir(
                        step.params["ticker"], company_name
                    )
                else:
                    self.context["ir_releases_raw"] = read_sample_ir(
                        step.params["ticker"], step.params["date"]
                    )

            case StepType.LOAD_NEWS:
                if use_live_data:
                    # First fetch stock info for company name
                    if "stock_info" not in self.context:
                        self.context["stock_info"] = fetch_live_stock_info(step.params["ticker"])
                    stock_info = self.context["stock_info"]
                    company_name = stock_info.get("name", "")
                    self.context["news_raw"] = fetch_live_news(step.params["ticker"], company_name)
                else:
                    self.context["news_raw"] = read_sample_news(
                        step.params["ticker"], step.params["date"]
                    )

            case StepType.SELECT_ITEMS:
                if step.params["source"] == "ir":
                    self.context["ir_releases"] = select_top_items(
                        self.context["ir_releases_raw"], step.params["n"]
                    )
                else:
                    self.context["news"] = select_top_items(
                        self.context["news_raw"], step.params["n"]
                    )

            case StepType.GENERATE_SECTIONS:
                context_for_llm = {
                    "ticker": self.context["ticker"],
                    "date": self.context["date"],
                    "ir_releases": self.context["ir_releases"],
                    "news": self.context["news"],
                }
                self.context["generated_sections"] = llm_generate_sections(
                    self.llm, context_for_llm
                )

            case StepType.RENDER_OUTPUT:
                # Build the BriefOutput model
                sections = self.context["generated_sections"]

                ir_models = [
                    IRRelease(
                        title=ir.get("title", ""),
                        date=ir.get("date", ""),
                        source=ir.get("source", ""),
                        url=ir.get("url", ""),
                        summary=ir.get("summary"),
                    )
                    for ir in self.context["ir_releases"]
                ]

                news_models = [
                    NewsItem(
                        title=n.get("title", ""),
                        source=n.get("source", ""),
                        url=n.get("url", ""),
                        date=n.get("date"),
                        summary=n.get("summary"),
                    )
                    for n in self.context["news"]
                ]

                self.context["brief"] = BriefOutput(
                    date=self.context["date"],
                    ticker=self.context["ticker"],
                    summary_bullets=sections.get("summary_bullets", []),
                    ir_releases=ir_models,
                    news=news_models,
                    drivers=sections.get("drivers", []),
                    risks=sections.get("risks", []),
                    limitations=sections.get("limitations", []),
                )

            case StepType.VALIDATE:
                # Validation is done in reflect phase
                pass

            case StepType.SAVE:
                if self.context.get("brief"):
                    paths = write_output_files(
                        self.context["brief"], step.params.get("output_dir", "output")
                    )
                    self.context["output_paths"] = paths
