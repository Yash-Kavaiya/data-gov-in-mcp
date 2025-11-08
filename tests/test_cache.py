"""
Tests for cache module
"""

import time
import pytest
from src.data_gov_in.cache import Cache, CacheEntry


class TestCacheEntry:
    """Test CacheEntry functionality"""

    def test_cache_entry_not_expired(self):
        """Test that fresh cache entry is not expired"""
        entry = CacheEntry("test_value", ttl=10)
        assert not entry.is_expired()
        assert entry.value == "test_value"

    def test_cache_entry_expired(self):
        """Test that expired cache entry is detected"""
        entry = CacheEntry("test_value", ttl=0)
        time.sleep(0.1)
        assert entry.is_expired()


class TestCache:
    """Test Cache functionality"""

    def test_cache_set_and_get(self):
        """Test basic set and get operations"""
        cache = Cache(max_size=10, default_ttl=60)

        cache.set("key1", "value1")
        result = cache.get("key1")

        assert result == "value1"

    def test_cache_miss(self):
        """Test cache miss returns None"""
        cache = Cache(max_size=10, default_ttl=60)
        result = cache.get("nonexistent")

        assert result is None

    def test_cache_expiry(self):
        """Test that expired entries are not returned"""
        cache = Cache(max_size=10, default_ttl=0)

        cache.set("key1", "value1")
        time.sleep(0.1)

        result = cache.get("key1")
        assert result is None

    def test_cache_max_size(self):
        """Test that cache respects max size (LRU eviction)"""
        cache = Cache(max_size=3, default_ttl=60)

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        cache.set("key4", "value4")  # Should evict key1

        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
        assert cache.get("key4") == "value4"

    def test_cache_lru_ordering(self):
        """Test LRU ordering is maintained"""
        cache = Cache(max_size=3, default_ttl=60)

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")

        # Access key1 to make it recently used
        cache.get("key1")

        # Add new key, should evict key2 (least recently used)
        cache.set("key4", "value4")

        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None
        assert cache.get("key3") == "value3"
        assert cache.get("key4") == "value4"

    def test_cache_clear(self):
        """Test cache clear"""
        cache = Cache(max_size=10, default_ttl=60)

        cache.set("key1", "value1")
        cache.set("key2", "value2")

        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None
        assert len(cache._cache) == 0

    def test_cache_stats(self):
        """Test cache statistics"""
        cache = Cache(max_size=10, default_ttl=60)

        cache.set("key1", "value1")

        # Hit
        cache.get("key1")
        # Miss
        cache.get("key2")

        stats = cache.stats()

        assert stats["size"] == 1
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert "hit_rate" in stats

    def test_cache_make_key(self):
        """Test cache key generation"""
        cache = Cache(max_size=10, default_ttl=60)

        key1 = cache._make_key("arg1", "arg2", kwarg1="value1")
        key2 = cache._make_key("arg1", "arg2", kwarg1="value1")
        key3 = cache._make_key("arg1", "arg3", kwarg1="value1")

        # Same arguments should produce same key
        assert key1 == key2
        # Different arguments should produce different key
        assert key1 != key3

    def test_cache_update_existing_key(self):
        """Test updating existing key"""
        cache = Cache(max_size=10, default_ttl=60)

        cache.set("key1", "value1")
        cache.set("key1", "value2")

        result = cache.get("key1")
        assert result == "value2"
        assert len(cache._cache) == 1

    def test_cache_custom_ttl(self):
        """Test custom TTL for individual entries"""
        cache = Cache(max_size=10, default_ttl=60)

        cache.set("key1", "value1", ttl=0)
        time.sleep(0.1)

        assert cache.get("key1") is None
