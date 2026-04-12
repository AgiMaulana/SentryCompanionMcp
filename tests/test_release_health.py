import pytest
from unittest.mock import patch, MagicMock

from sentry_companion_mcp.tools.release_health import (
    get_release_health,
    get_release_adoption,
)


@pytest.fixture
def mock_config():
    return {
        "org": "test-org",
        "project": "test-project",
        "token": "test-token",
        "base_url": "https://sentry.io",
    }


@pytest.fixture
def mock_sentry_response():
    return {
        "groups": [
            {
                "by": {"release": "com.app@1.0.0"},
                "totals": {
                    "sum(session)": 1000,
                    "count_unique(user)": 500,
                    "crash_free_rate(session)": 0.95,
                    "crash_free_rate(user)": 0.92,
                },
            },
        ]
    }


class TestGetReleaseHealth:
    @patch("sentry_companion_mcp.tools.release_health.get_config")
    @patch("sentry_companion_mcp.tools.release_health.sentry_get")
    def test_returns_str_when_data_found(
        self, mock_sentry_get, mock_get_config, mock_config, mock_sentry_response
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = mock_sentry_response

        result = get_release_health("1.0", days=3)

        assert isinstance(result, str)
        assert "com.app@1.0.0" in result


class TestGetReleaseAdoption:
    @patch("sentry_companion_mcp.tools.release_health.get_config")
    @patch("sentry_companion_mcp.tools.release_health.sentry_get")
    def test_returns_str_when_data_found(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = {
            "groups": [
                {
                    "by": {"release": "com.app@1.0.0"},
                    "totals": {
                        "sum(session)": 1000,
                        "count_unique(user)": 500,
                    },
                },
                {
                    "by": {"release": "com.app@2.0.0"},
                    "totals": {
                        "sum(session)": 500,
                        "count_unique(user)": 250,
                    },
                },
            ]
        }

        result = get_release_adoption("1.0", days=3)

        assert isinstance(result, str)
        assert "com.app@1.0.0" in result


from sentry_companion_mcp.tools.release_health import compare_releases


class TestCompareReleases:
    @patch("sentry_companion_mcp.tools.release_health.get_config")
    @patch("sentry_companion_mcp.tools.release_health.sentry_get")
    def test_returns_str_when_both_found(self, mock_sentry_get, mock_get_config):
        mock_get_config.return_value = {
            "org": "test-org",
            "project": "test-project",
            "token": "test-token",
            "base_url": "https://sentry.io",
        }
        mock_sentry_get.return_value = {
            "groups": [
                {
                    "by": {"release": "com.app@1.0.0"},
                    "totals": {
                        "sum(session)": 1000,
                        "count_unique(user)": 500,
                        "crash_free_rate(session)": 0.95,
                        "crash_free_rate(user)": 0.90,
                    },
                },
                {
                    "by": {"release": "com.app@2.0.0"},
                    "totals": {
                        "sum(session)": 2000,
                        "count_unique(user)": 800,
                        "crash_free_rate(session)": 0.98,
                        "crash_free_rate(user)": 0.95,
                    },
                },
            ]
        }

        result = compare_releases("1.0", "2.0", days=7)

        assert isinstance(result, str)
        assert "com.app@1.0.0" in result

    @patch("sentry_companion_mcp.tools.release_health.get_config")
    @patch("sentry_companion_mcp.tools.release_health.sentry_get")
    def test_returns_str_when_one_not_found(self, mock_sentry_get, mock_get_config):
        mock_get_config.return_value = {
            "org": "test-org",
            "project": "test-project",
            "token": "test-token",
            "base_url": "https://sentry.io",
        }
        mock_sentry_get.return_value = {
            "groups": [
                {
                    "by": {"release": "com.app@1.0.0"},
                    "totals": {
                        "sum(session)": 1000,
                        "count_unique(user)": 500,
                        "crash_free_rate(session)": 0.95,
                        "crash_free_rate(user)": 0.90,
                    },
                },
            ]
        }

        result = compare_releases("1.0", "nonexistent", days=7)

        assert isinstance(result, str)
