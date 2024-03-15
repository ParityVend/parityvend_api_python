from parityvend_api.cache.default import DefaultCache


def _get_new_cache():
    return DefaultCache(maxsize=4, ttl=8)


def test_contains():
    cache = _get_new_cache()
    cache["foo"] = "bar"
    assert "foo" in cache


def test_get():
    cache = _get_new_cache()
    cache["foo"] = "bar"
    assert cache["foo"] == "bar"
