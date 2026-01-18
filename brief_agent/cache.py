"""File-based caching for API responses and computed results."""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .utils import get_logger


class FileCache:
    """Simple file-based cache with TTL support."""

    def __init__(self, cache_dir: Path | str = ".cache", ttl_hours: int = 24):
        """
        Initialize the file cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live for cache entries in hours
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.logger = get_logger()

    def _get_cache_key(self, key: str) -> str:
        """Generate a safe filename from a cache key."""
        return hashlib.md5(key.encode()).hexdigest()

    def _get_cache_path(self, key: str) -> Path:
        """Get the full path for a cache entry."""
        return self.cache_dir / f"{self._get_cache_key(key)}.json"

    def get(self, key: str) -> Any | None:
        """
        Retrieve a value from the cache.

        Args:
            key: Cache key

        Returns:
            Cached value if found and not expired, None otherwise
        """
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check TTL
            cached_time = datetime.fromisoformat(data["timestamp"])
            if datetime.now() - cached_time > self.ttl:
                self.logger.debug(f"Cache expired for key: {key[:20]}...")
                cache_path.unlink()
                return None

            self.logger.debug(f"Cache hit for key: {key[:20]}...")
            return data["value"]

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.warning(f"Invalid cache entry: {e}")
            cache_path.unlink(missing_ok=True)
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Store a value in the cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON-serializable)
        """
        cache_path = self._get_cache_path(key)

        data = {"timestamp": datetime.now().isoformat(), "value": value}

        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug(f"Cached value for key: {key[:20]}...")
        except (TypeError, ValueError) as e:
            self.logger.warning(f"Failed to cache value: {e}")

    def clear(self) -> int:
        """
        Clear all cache entries.

        Returns:
            Number of entries cleared
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        self.logger.info(f"Cleared {count} cache entries")
        return count

    def clear_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cached_time = datetime.fromisoformat(data["timestamp"])
                if datetime.now() - cached_time > self.ttl:
                    cache_file.unlink()
                    count += 1
            except Exception:
                cache_file.unlink(missing_ok=True)
                count += 1

        if count:
            self.logger.info(f"Removed {count} expired cache entries")
        return count
