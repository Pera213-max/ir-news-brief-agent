"""Planner module for generating execution steps."""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .utils import get_logger


class StepType(Enum):
    """Types of execution steps."""

    LOAD_IR = "load_ir"
    LOAD_NEWS = "load_news"
    SELECT_ITEMS = "select_items"
    GENERATE_SECTIONS = "generate_sections"
    RENDER_OUTPUT = "render_output"
    VALIDATE = "validate"
    SAVE = "save"


@dataclass
class PlanStep:
    """A single step in the execution plan."""

    step_type: StepType
    description: str
    params: dict[str, Any]

    def __str__(self) -> str:
        return f"[{self.step_type.value}] {self.description}"


class Planner:
    """
    Planner that generates ordered execution steps for the agent.
    Given a goal, produces a list of steps to achieve it.
    """

    def __init__(self):
        self.logger = get_logger()

    def plan(self, goal: dict[str, Any]) -> list[PlanStep]:
        """
        Generate an execution plan based on the goal.

        Args:
            goal: Dictionary containing 'ticker', 'date', and optionally 'mode'

        Returns:
            Ordered list of PlanStep objects
        """
        ticker = goal.get("ticker", "UNKNOWN")
        date = goal.get("date", "")
        mode = goal.get("mode", "demo")

        self.logger.info(f"Planning brief generation for {ticker} on {date} (mode: {mode})")

        steps = [
            PlanStep(
                step_type=StepType.LOAD_IR,
                description=f"Load IR releases for {ticker}",
                params={"ticker": ticker, "date": date},
            ),
            PlanStep(
                step_type=StepType.LOAD_NEWS,
                description=f"Load news items for {ticker}",
                params={"ticker": ticker, "date": date},
            ),
            PlanStep(
                step_type=StepType.SELECT_ITEMS,
                description="Select top IR releases (3 items)",
                params={"source": "ir", "n": 3},
            ),
            PlanStep(
                step_type=StepType.SELECT_ITEMS,
                description="Select top news items (5 items)",
                params={"source": "news", "n": 5},
            ),
            PlanStep(
                step_type=StepType.GENERATE_SECTIONS,
                description="Generate summary, drivers, and risks via LLM",
                params={"mode": mode},
            ),
            PlanStep(
                step_type=StepType.RENDER_OUTPUT,
                description="Render markdown and prepare JSON",
                params={"ticker": ticker, "date": date},
            ),
            PlanStep(
                step_type=StepType.VALIDATE,
                description="Validate output contains all required sections",
                params={},
            ),
            PlanStep(
                step_type=StepType.SAVE,
                description="Save MD and JSON files to output directory",
                params={"output_dir": "output"},
            ),
        ]

        self.logger.info(f"Generated plan with {len(steps)} steps")
        for i, step in enumerate(steps, 1):
            self.logger.debug(f"  Step {i}: {step}")

        return steps
