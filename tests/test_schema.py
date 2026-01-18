"""Tests for JSON schema validation."""

import pytest
from pydantic import ValidationError

from brief_agent.schemas import BriefOutput, IRRelease, NewsItem


class TestIRRelease:
    """Tests for IRRelease schema."""

    def test_valid_ir_release(self):
        """Test creating a valid IR release."""
        ir = IRRelease(
            title="Q4 Earnings Report",
            date="2026-01-17",
            source="Nokia IR",
            url="https://nokia.com/ir",
        )
        assert ir.title == "Q4 Earnings Report"
        assert ir.source == "Nokia IR"

    def test_ir_release_with_summary(self):
        """Test IR release with optional summary."""
        ir = IRRelease(
            title="Partnership Announcement",
            date="2026-01-15",
            source="Nokia IR",
            url="https://nokia.com/news",
            summary="Strategic partnership with AWS announced.",
        )
        assert ir.summary == "Strategic partnership with AWS announced."

    def test_ir_release_missing_required(self):
        """Test that missing required fields raise error."""
        with pytest.raises(ValidationError):
            IRRelease(title="Test", date="2026-01-17")  # Missing source and url


class TestNewsItem:
    """Tests for NewsItem schema."""

    def test_valid_news_item(self):
        """Test creating a valid news item."""
        news = NewsItem(
            title="Stock Surges",
            source="Reuters",
            url="https://reuters.com/news",
        )
        assert news.title == "Stock Surges"

    def test_news_item_with_optionals(self):
        """Test news item with all optional fields."""
        news = NewsItem(
            title="Tech Rally",
            source="Bloomberg",
            url="https://bloomberg.com",
            date="2026-01-18",
            summary="European tech stocks rally.",
        )
        assert news.date == "2026-01-18"
        assert news.summary == "European tech stocks rally."


class TestBriefOutput:
    """Tests for BriefOutput schema."""

    def test_valid_brief_output(self):
        """Test creating a valid brief output."""
        brief = BriefOutput(
            date="2026-01-18",
            ticker="NOKIA.HE",
            summary_bullets=["Point 1", "Point 2", "Point 3"],
            ir_releases=[
                IRRelease(
                    title="Earnings",
                    date="2026-01-17",
                    source="IR",
                    url="https://example.com",
                )
            ],
            news=[
                NewsItem(
                    title="News Article",
                    source="News Site",
                    url="https://news.com",
                )
            ],
            drivers=["Strong demand"],
            risks=["Competition"],
            limitations=["Demo mode"],
        )
        assert brief.ticker == "NOKIA.HE"
        assert len(brief.summary_bullets) == 3

    def test_brief_json_serialization(self):
        """Test that brief can be serialized to JSON."""
        brief = BriefOutput(
            date="2026-01-18",
            ticker="NOKIA.HE",
            summary_bullets=["Bullet 1", "Bullet 2", "Bullet 3"],
            ir_releases=[],
            news=[],
            drivers=["Driver 1"],
            risks=["Risk 1"],
            limitations=["Limitation 1"],
        )
        json_str = brief.model_dump_json()
        assert '"ticker": "NOKIA.HE"' in json_str
        assert "2026-01-18" in json_str
