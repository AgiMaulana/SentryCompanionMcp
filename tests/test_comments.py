import pytest
from unittest.mock import patch, MagicMock

from sentry_companion_mcp.tools.comments import add_issue_comment


@pytest.fixture
def mock_config():
    return {
        "org": "test-org",
        "project": "test-project",
        "token": "test-token",
        "base_url": "https://sentry.io",
    }


class TestAddIssueComment:
    @patch("sentry_companion_mcp.tools.comments.get_config")
    @patch("sentry_companion_mcp.tools.comments.sentry_post")
    @patch("sentry_companion_mcp.tools.comments.sentry_get")
    def test_returns_dict_when_comment_posted(
        self, mock_sentry_get, mock_sentry_post, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_get.return_value = [{"id": "1234567890"}]
        mock_sentry_post.return_value = {"id": "comment-123"}

        result = add_issue_comment("TEST-1", "Test comment")

        assert isinstance(result, dict)
        assert "comment_id" in result
        assert result["comment_id"] == "comment-123"

    @patch("sentry_companion_mcp.tools.comments.get_config")
    @patch("sentry_companion_mcp.tools.comments.sentry_post")
    def test_returns_dict_with_numeric_id(
        self, mock_sentry_post, mock_get_config, mock_config
    ):
        mock_get_config.return_value = mock_config
        mock_sentry_post.return_value = {"id": "comment-456"}

        result = add_issue_comment("1234567890", "Test comment")

        assert isinstance(result, dict)
        assert "comment_id" in result
