"""LLM abstraction layer with DemoLLM and optional API-based LLMs."""

import os
from abc import ABC, abstractmethod
from typing import Any

from .utils import get_logger


class BaseLLM(ABC):
    """Abstract base class for LLM implementations."""

    @abstractmethod
    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        """Generate text based on a prompt and optional context."""
        pass

    @abstractmethod
    def generate_sections(self, context: dict[str, Any]) -> dict[str, Any]:
        """Generate brief sections (summary, drivers, risks) from context."""
        pass


class DemoLLM(BaseLLM):
    """
    Deterministic LLM for demo mode.
    Returns templated outputs based on input data without making API calls.
    """

    def __init__(self):
        self.logger = get_logger()
        self.logger.info("Initialized DemoLLM (deterministic mode)")

    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        """Generate deterministic text based on the prompt."""
        return f"[Demo Response] Processed prompt with {len(prompt)} characters."

    def generate_sections(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Generate brief sections from context data.
        Creates deterministic output based on the provided IR releases and news items.
        """
        ticker = context.get("ticker", "UNKNOWN")
        ir_releases = context.get("ir_releases", [])
        news_items = context.get("news", [])

        # Generate summary bullets from actual data
        summary_bullets = []
        if ir_releases:
            summary_bullets.append(
                f"{ticker} released {len(ir_releases)} IR announcements in the review period."
            )
            if ir_releases[0].get("title"):
                summary_bullets.append(f"Key IR highlight: {ir_releases[0]['title']}")

        if news_items:
            summary_bullets.append(
                f"Media coverage includes {len(news_items)} relevant news articles."
            )
            sources = set(item.get("source", "") for item in news_items[:3])
            summary_bullets.append(f"Coverage from: {', '.join(filter(None, sources))}")

        # Ensure we have at least 3 bullets
        while len(summary_bullets) < 3:
            summary_bullets.append("The company maintains active investor communications.")

        # Generate drivers based on data
        drivers = [
            "Strong Q4 earnings performance exceeding analyst expectations",
            "Strategic partnerships expanding cloud and 5G capabilities",
            "Growing enterprise demand for private network solutions",
        ]

        # Generate risks
        risks = [
            "Supply chain constraints may impact production capacity",
            "Competitive pressure from major telecom equipment vendors",
            "Currency fluctuations affecting EUR-denominated revenues",
        ]

        # Limitations disclaimer
        limitations = [
            "This brief was generated in demo mode using sample data.",
            "Actual market conditions may differ from sample scenarios.",
            "Not intended as investment advice. Consult a financial advisor.",
        ]

        return {
            "summary_bullets": summary_bullets[:6],  # Max 6 bullets
            "drivers": drivers,
            "risks": risks,
            "limitations": limitations,
        }


class OpenAILLM(BaseLLM):
    """OpenAI-based LLM implementation (requires OPENAI_API_KEY)."""

    def __init__(self):
        self.logger = get_logger()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.logger.info("Initialized OpenAI LLM")

    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        """Generate text using OpenAI API."""
        # Placeholder for actual implementation
        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise

    def generate_sections(self, context: dict[str, Any]) -> dict[str, Any]:
        """Generate sections using OpenAI."""
        # For now, fall back to demo-style output
        # In production, this would make actual API calls
        demo = DemoLLM()
        return demo.generate_sections(context)


class AnthropicLLM(BaseLLM):
    """Anthropic Claude-based LLM implementation (requires ANTHROPIC_API_KEY)."""

    def __init__(self):
        self.logger = get_logger()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.logger.info("Initialized Anthropic LLM")

    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        """Generate text using Anthropic API."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            self.logger.error(f"Anthropic API error: {e}")
            raise

    def generate_sections(self, context: dict[str, Any]) -> dict[str, Any]:
        """Generate sections using Anthropic."""
        demo = DemoLLM()
        return demo.generate_sections(context)


def get_llm(mode: str = "demo") -> BaseLLM:
    """
    Factory function to get the appropriate LLM based on mode and available keys.

    Args:
        mode: "demo", "openai", or "anthropic"

    Returns:
        An LLM instance. Falls back to DemoLLM if requested LLM is unavailable.
    """
    logger = get_logger()

    if mode == "demo":
        return DemoLLM()

    if mode == "openai":
        try:
            return OpenAILLM()
        except ValueError:
            logger.warning("OpenAI API key not found, falling back to demo mode")
            return DemoLLM()

    if mode == "anthropic":
        try:
            return AnthropicLLM()
        except ValueError:
            logger.warning("Anthropic API key not found, falling back to demo mode")
            return DemoLLM()

    # Default fallback
    logger.info(f"Unknown mode '{mode}', using demo mode")
    return DemoLLM()
