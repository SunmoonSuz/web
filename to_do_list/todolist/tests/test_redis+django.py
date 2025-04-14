from django.core.cache import cache

def test_redis_cache():
    cache.set("test_key", "value", timeout=10)
    assert cache.get("test_key") == "value"