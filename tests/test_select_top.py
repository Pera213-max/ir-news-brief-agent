"""Tests for item selection logic."""

from brief_agent.tools import select_top_items


class TestSelectTopItems:
    """Tests for select_top_items function."""

    def test_select_top_n(self):
        """Test selecting top N items."""
        items = [
            {"title": "Item 1", "date": "2026-01-15"},
            {"title": "Item 2", "date": "2026-01-17"},
            {"title": "Item 3", "date": "2026-01-16"},
        ]
        result = select_top_items(items, n=2)
        assert len(result) == 2
        # Should be sorted by date descending
        assert result[0]["date"] == "2026-01-17"
        assert result[1]["date"] == "2026-01-16"

    def test_select_with_fewer_items(self):
        """Test when fewer items exist than requested."""
        items = [{"title": "Only Item", "date": "2026-01-18"}]
        result = select_top_items(items, n=5)
        assert len(result) == 1

    def test_select_empty_list(self):
        """Test with empty input list."""
        result = select_top_items([], n=3)
        assert result == []

    def test_select_preserves_data(self):
        """Test that item data is preserved."""
        items = [
            {"title": "Test", "date": "2026-01-18", "url": "https://example.com"},
        ]
        result = select_top_items(items, n=1)
        assert result[0]["url"] == "https://example.com"

    def test_select_handles_missing_sort_field(self):
        """Test graceful handling of missing sort field."""
        items = [
            {"title": "Item 1"},
            {"title": "Item 2", "date": "2026-01-17"},
        ]
        # Should not raise error
        result = select_top_items(items, n=2)
        assert len(result) == 2
