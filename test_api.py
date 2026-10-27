import importlib
import logging
import os
from unittest.mock import patch, MagicMock
from api import mangle_redis_url, logger


def test_mangle_redis_url_with_password():
    url_with_pass = "redis://:secretpass@localhost:6379/0"
    mangled = mangle_redis_url(url_with_pass)
    assert "secretpass" not in mangled
    assert mangled == "redis://:***@localhost:6379/0"

    url_user_pass = "redis://admin:secretpass@127.0.0.1:6379/1"
    mangled_user = mangle_redis_url(url_user_pass)
    assert "secretpass" not in mangled_user
    assert mangled_user == "redis://admin:***@127.0.0.1:6379/1"


def test_mangle_redis_url_without_password():
    url_no_pass = "redis://localhost:6379/0"
    assert mangle_redis_url(url_no_pass) == "redis://localhost:6379/0"

    empty_url = ""
    assert mangle_redis_url(empty_url) == ""


def test_redis_startup_logging_with_redis(caplog):
    test_url = "redis://:secret123@redis-server:6379/0"
    with patch.dict(os.environ, {"REDIS_URL": test_url}):
        with patch("redis.from_url") as mock_redis:
            mock_client = MagicMock()
            mock_redis.return_value = mock_client
            with caplog.at_level(logging.INFO):
                import api
                importlib.reload(api)

            assert "Starting with REDIS: redis://:***@redis-server:6379/0" in caplog.text
            assert "secret123" not in caplog.text


def test_redis_startup_logging_without_redis(caplog):
    with patch.dict(os.environ, {}, clear=True):
        if "REDIS_URL" in os.environ:
            del os.environ["REDIS_URL"]
        with caplog.at_level(logging.INFO):
            import api
            importlib.reload(api)

        assert "Starting without REDIS" in caplog.text
