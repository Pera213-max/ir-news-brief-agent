"""Pydantic schemas for JSON output validation."""

from typing import Optional

from pydantic import BaseModel, Field


class IRRelease(BaseModel):
    """Schema for an IR release item."""

    title: str = Field(..., description="Title of the IR release")
    date: str = Field(..., description="Publication date (YYYY-MM-DD)")
    source: str = Field(..., description="Source of the release")
    url: str = Field(..., description="URL to the full release")
    summary: Optional[str] = Field(None, description="Brief summary of the release")


class NewsItem(BaseModel):
    """Schema for a news item."""

    title: str = Field(..., description="News headline")
    source: str = Field(..., description="News source/publication")
    url: str = Field(..., description="URL to the article")
    date: Optional[str] = Field(None, description="Publication date if available")
    summary: Optional[str] = Field(None, description="Brief summary of the article")


class BriefOutput(BaseModel):
    """Schema for the complete brief JSON output."""

    date: str = Field(..., description="Date of the brief (YYYY-MM-DD)")
    ticker: str = Field(..., description="Stock ticker symbol")
    summary_bullets: list[str] = Field(
        ..., description="3-6 bullet points summarizing key information"
    )
    ir_releases: list[IRRelease] = Field(..., description="Top IR releases")
    news: list[NewsItem] = Field(..., description="Top news items")
    drivers: list[str] = Field(..., description="Key drivers identified by LLM")
    risks: list[str] = Field(..., description="Key risks identified by LLM")
    limitations: list[str] = Field(..., description="Notes and limitations disclaimer")

    model_config = {"json_schema_extra": {"example": {"date": "2026-01-18", "ticker": "NOKIA.HE"}}}
