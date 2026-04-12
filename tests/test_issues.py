import pytest
from unittest.mock import patch

from sentry_companion_mcp.tools.issues import (
    get_release_new_issues,
    get_release_regressed_issues,
    get_issue_users,
)


@pytest.fixture
def mock_config():
    return {
        "org": "test-org",
        "project": "test-project",
        "token": "test-token",
        "base_url": "https://sentry.io",
    }


class TestGetReleaseNewIssues:
    @patch("sentry_companion_mcp.tools.issues.get_config")
    @patch("sentry_companion_mcp.tools.issues.sentry_get")
    def test_returns_str_when_issues_found(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = [
            {"id": "123", "title": "Test error", "count": 5, "culprit": "main.js"},
        ]

        result = get_release_new_issues("com.app@1.0.0")

        assert isinstance(result, str)
        assert "Test error" in result

    @patch("sentry_companion_mcp.tools.issues.get_config")
    @patch("sentry_companion_mcp.tools.issues.sentry_get")
    def test_returns_str_when_no_issues(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = []

        result = get_release_new_issues("com.app@1.0.0")

        assert isinstance(result, str)


class TestGetReleaseRegressedIssues:
    @patch("sentry_companion_mcp.tools.issues.get_config")
    @patch("sentry_companion_mcp.tools.issues.sentry_get")
    def test_returns_str_when_issues_found(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = [
            {"id": "456", "title": "Regressed error", "count": 10, "culprit": "app.js"},
        ]

        result = get_release_regressed_issues("com.app@1.0.0")

        assert isinstance(result, str)
        assert "Regressed error" in result

    @patch("sentry_companion_mcp.tools.issues.get_config")
    @patch("sentry_companion_mcp.tools.issues.sentry_get")
    def test_returns_str_when_no_issues(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = []

        result = get_release_regressed_issues("com.app@1.0.0")

        assert isinstance(result, str)


class TestGetIssueUsers:
    @patch("sentry_companion_mcp.tools.issues.get_config")
    @patch("sentry_companion_mcp.tools.issues.sentry_get")
    def test_returns_dict_with_compact_json(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = [
            {"user": {"email": "test1@example.com", "id": "u1"}},
            {"user": {"email": "test2@example.com", "id": "u2"}},
        ]

        result = get_issue_users("123")

        assert isinstance(result, dict)
        assert "issue_id" in result
        assert "unique_users" in result

        import json

        json_str = json.dumps(result)
        assert "\n" not in json_str

    @patch("sentry_companion_mcp.tools.issues.get_config")
    @patch("sentry_companion_mcp.tools.issues.sentry_get")
    def test_returns_str_when_no_events(
        self, mock_sentry_get, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = []

        result = get_issue_users("123")

        assert isinstance(result, str)
