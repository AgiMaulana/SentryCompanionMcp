import pytest
from unittest.mock import patch

from sentry_companion_mcp.tools.deploys import get_release_deploys


@pytest.fixture
def mock_config():
    return {
        "org": "test-org",
        "project": "test-project",
        "token": "test-token",
        "base_url": "https://sentry.io",
    }


class TestGetReleaseDeploys:
    @patch("sentry_companion_mcp.tools.deploys.get_config")
    @patch("sentry_companion_mcp.tools.deploys.sentry_get")
    def test_returns_str_when_deploys_found(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = [
            {"id": "d1", "environment": "production", "dateFinished": "2024-01-01"},
            {"id": "d2", "environment": "staging", "dateFinished": "2024-01-02"},
        ]

        result = get_release_deploys("com.app@1.0.0")

        assert isinstance(result, str)
        assert "Deployments for" in result

    @patch("sentry_companion_mcp.tools.deploys.get_config")
    @patch("sentry_companion_mcp.tools.deploys.sentry_get")
    def test_returns_str_when_no_deploys(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = []

        result = get_release_deploys("com.app@1.0.0")

        assert isinstance(result, str)
