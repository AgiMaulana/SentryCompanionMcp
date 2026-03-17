import urllib.parse
from ..client import get_config, sentry_get, sentry_post


def add_issue_comment(issue_id: str, text: str) -> str:
    """
    Post a comment on a Sentry issue.
    Fills the gap in both the official Sentry MCP and this companion — neither
    exposes a comment endpoint.

    The issue_id can be either:
    - A short ID (e.g. "GOOD-DOCTOR-ANDROID-6YW") — resolved automatically via the org API
    - A numeric ID (e.g. "7295890684") — used directly

    Args:
        issue_id: Short issue ID (e.g. "PROJ-1AB") or numeric ID (e.g. "1234567890")
        text: Comment body (plain text)
    """
    cfg = get_config()
    numeric_id = _resolve_issue_id(cfg, issue_id)
    result = sentry_post(
        f"/api/0/issues/{numeric_id}/comments/",
        {"text": text},
        cfg["token"],
        cfg["base_url"],
    )
    comment_id = result.get("id", "")
    return f"Comment posted (id={comment_id}) on issue {issue_id}."


def _resolve_issue_id(cfg: dict, issue_id: str) -> str:
    """Return the numeric issue ID. Resolves short IDs (e.g. PROJ-1AB) via the org API."""
    if issue_id.isdigit():
        return issue_id
    encoded = urllib.parse.quote(issue_id)
    path = f"/api/0/organizations/{cfg['org']}/issues/?shortId={encoded}&limit=1"
    result = sentry_get(path, cfg["token"], cfg["base_url"])
    if isinstance(result, list) and result:
        return str(result[0]["id"])
    if isinstance(result, dict) and "id" in result:
        return str(result["id"])
    raise ValueError(f"Could not resolve Sentry issue ID: {issue_id}")
