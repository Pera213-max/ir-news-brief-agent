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
        Creates Finnish output based on the provided IR releases and news items.
        """
        ticker = context.get("ticker", "UNKNOWN")
        ir_releases = context.get("ir_releases", [])
        news_items = context.get("news", [])

        # Generate summary bullets from actual data (Finnish)
        summary_bullets = []

        # Add context-aware summaries based on actual news
        if news_items:
            # Get first news item for summary
            first_news = news_items[0]
            title = first_news.get("title", "")
            if title:
                summary_bullets.append(f"Uutinen: {title[:100]}...")

            summary_bullets.append(f"Löydettiin {len(news_items)} uutista yrityksestä {ticker}.")
            sources = set(item.get("source", "") for item in news_items[:3])
            if sources:
                summary_bullets.append(f"Lähteet: {', '.join(filter(None, sources))}")

        if ir_releases:
            summary_bullets.append(f"IR-tiedotteita: {len(ir_releases)} kpl tarkastelujaksolla.")
            if ir_releases[0].get("title"):
                ir_title = ir_releases[0]["title"][:80]
                summary_bullets.append(f"Tärkein tiedote: {ir_title}")

        # Ensure we have at least 3 bullets
        while len(summary_bullets) < 3:
            summary_bullets.append(f"Analyysi perustuu julkisiin uutisiin yrityksestä {ticker}.")

        # Generate drivers based on actual news content (Finnish)
        drivers = []
        for item in news_items[:3]:
            title = item.get("title", "")
            if title:
                # Create a driver-style bullet from news
                drivers.append(f"Uutisanalyysi: {title[:80]}")

        # Add generic drivers if not enough
        while len(drivers) < 3:
            drivers.append("Lisätietoja saatavilla yhtiön sijoittajasivuilta.")

        # Generate risks (Finnish) - based on general market
        risks = [
            "Markkinatilanne voi vaikuttaa osakekurssiin",
            "Toimialaan liittyvät yleiset riskit",
            "Valuuttakurssien ja korkojen vaikutus tulokseen",
        ]

        # Limitations disclaimer (Finnish)
        limitations = [
            f"Tiivistelmä perustuu automaattiseen uutishakuun.",
            "Analyysi ei ole sijoitussuositus.",
            "Tarkista tiedot yhtiön virallisista lähteistä.",
        ]

        return {
            "summary_bullets": summary_bullets[:6],  # Max 6 bullets
            "drivers": drivers[:3],
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


class GeminiLLM(BaseLLM):
    """Google Gemini-based LLM implementation (requires GEMINI_API_KEY)."""

    def __init__(self):
        self.logger = get_logger()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        self.logger.info("Initialized Gemini LLM")

    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        """Generate text using Gemini API."""
        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text or ""
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            raise

    def generate_sections(self, context: dict[str, Any]) -> dict[str, Any]:
        """Generate sections using Gemini."""
        ticker = context.get("ticker", "UNKNOWN")
        ir_releases = context.get("ir_releases", [])
        news_items = context.get("news", [])

        # Build prompt for Gemini - Finnish output
        prompt = f"""Olet talousanalyytikko, joka luo tiivistelmän yrityksestä {ticker}.

Alla olevan datan perusteella, luo SUOMEKSI:
1. summary_bullets: 3-6 tärkeintä huomiota (suomeksi)
2. drivers: 3 keskeistä kasvuajuria (suomeksi)
3. risks: 3 keskeistä riskiä (suomeksi)

IR-tiedotteet:
{self._format_items(ir_releases)}

Uutiset:
{self._format_items(news_items)}

Vastaa JSON-muodossa avaimilla: summary_bullets, drivers, risks, limitations.
Sisällytä limitations-taulukko varoituksilla analyysistä (suomeksi).
TÄRKEÄÄ: Kaikki tekstit SUOMEKSI."""

        try:
            response_text = self.generate(prompt)
            # Try to parse JSON from response
            import json
            import re

            # Extract JSON from response (may be wrapped in markdown code blocks)
            json_match = re.search(r"\{[\s\S]*\}", response_text)
            if json_match:
                result = json.loads(json_match.group())
                # Ensure all required keys exist
                return {
                    "summary_bullets": result.get("summary_bullets", [])[:6],
                    "drivers": result.get("drivers", []),
                    "risks": result.get("risks", []),
                    "limitations": result.get(
                        "limitations",
                        [
                            "Luotu tekoälyanalyysillä.",
                            "Ei sijoitusneuvontaa.",
                        ],
                    ),
                }
        except Exception as e:
            self.logger.warning(f"Failed to parse Gemini response: {e}, using demo fallback")

        # Fallback to demo if parsing fails
        demo = DemoLLM()
        return demo.generate_sections(context)

    def _format_items(self, items: list) -> str:
        """Format items for the prompt."""
        if not items:
            return "No items available."
        return "\n".join(
            f"- {item.get('title', 'No title')}: {item.get('summary', item.get('source', ''))}"
            for item in items[:5]
        )


def get_llm(mode: str = "demo") -> BaseLLM:
    """
    Factory function to get the appropriate LLM based on mode and available keys.

    Args:
        mode: "demo", "openai", "anthropic", or "gemini"

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

    if mode == "gemini":
        try:
            return GeminiLLM()
        except ValueError:
            logger.warning("Gemini API key not found, falling back to demo mode")
            return DemoLLM()

    # Default fallback
    logger.info(f"Unknown mode '{mode}', using demo mode")
    return DemoLLM()
