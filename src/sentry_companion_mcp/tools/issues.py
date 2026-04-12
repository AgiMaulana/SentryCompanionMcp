import json
import urllib.parse
from ..client import get_config, sentry_get


def get_release_new_issues(version: str, limit: int = 25) -> str:
    """
    List new issues (first seen) in a specific release.
    Complements the official Sentry MCP which searches issues but doesn't
    filter by firstSeen release directly.

    Args:
        version: Full release version (e.g. "com.pajk.idpersonaldoc@5.57.2-c52b693+50105")
        limit: Max number of issues to return (default: 25)
    """
    cfg = get_config()
    query = urllib.parse.quote(f"firstRelease:{version}")
    path = (
        f"/api/0/projects/{cfg['org']}/good-doctor-android/issues/"
        f"?query={query}&limit={limit}&sort=date"
    )
    issues = sentry_get(path, cfg["token"], cfg["base_url"])

    if not issues:
        return f"No new issues found for release '{version}'."

    lines = [f"New issues in {version} (up to {limit}):"]
    for issue in issues:
        title = issue.get("title", "Unknown")
        issue_id = issue.get("id", "")
        count = issue.get("count", 0)
        culprit = issue.get("culprit", "")
        url = f"{cfg['base_url']}/organizations/{cfg['org']}/issues/{issue_id}/"
        lines.append(f"  [{issue_id}] {title}")
        lines.append(f"    Culprit : {culprit}")
        lines.append(f"    Events  : {count}")
        lines.append(f"    URL     : {url}")
        lines.append("")

    return "\n".join(lines).strip()


def get_event_user_geo(issue_id: str, organization_slug: str = None, event_id: str = "latest") -> str:
    """
    Get the geo information for a user in a specific Sentry event.
    Fills the gap left by the official Sentry MCP which only returns hashed user IDs.

    Args:
        issue_id: The Sentry issue ID (e.g. "GOOD-DOCTOR-ANDROID-6XV")
        organization_slug: Organization slug (defaults to configured org)
        event_id: Event ID to fetch, defaults to "latest"
    """
    cfg = get_config()
    org = organization_slug or cfg["org"]
    path = f"/api/0/organizations/{org}/issues/{issue_id}/events/{event_id}/"

    event = sentry_get(path, cfg["token"], cfg["base_url"])

    user = event.get("user", {})
    geo = user.get("geo")

    if not geo:
        return (
            f"No geo information found for issue '{issue_id}' (event: {event_id}).\n"
            f"User ID: {user.get('id', 'N/A')}"
        )

    result = {
        "issue_id": issue_id,
        "event": event_id,
        "user_geo": {
            "country_code": geo.get("country_code"),
            "city": geo.get("city"),
            "region": geo.get("region"),
        },
    }

    # Remove None values
    result["user_geo"] = {k: v for k, v in result["user_geo"].items() if v is not None}

    return json.dumps(result, indent=2)


def get_release_regressed_issues(version: str, limit: int = 25) -> str:
    """
    List issues that regressed in a specific release.

    Args:
        version: Full release version (e.g. "com.pajk.idpersonaldoc@5.57.2-c52b693+50105")
        limit: Max number of issues to return (default: 25)
    """
    cfg = get_config()
    query = urllib.parse.quote(f"regressed_in_release:{version}")
    path = (
        f"/api/0/projects/{cfg['org']}/good-doctor-android/issues/"
        f"?query={query}&limit={limit}&sort=date"
    )
    issues = sentry_get(path, cfg["token"], cfg["base_url"])

    if not issues:
        return f"No regressed issues found for release '{version}'."

    lines = [f"Regressed issues in {version} (up to {limit}):"]
    for issue in issues:
        title = issue.get("title", "Unknown")
        issue_id = issue.get("id", "")
        count = issue.get("count", 0)
        culprit = issue.get("culprit", "")
        url = f"{cfg['base_url']}/organizations/{cfg['org']}/issues/{issue_id}/"
        lines.append(f"  [{issue_id}] {title}")
        lines.append(f"    Culprit : {culprit}")
        lines.append(f"    Events  : {count}")
        lines.append(f"    URL     : {url}")
        lines.append("")

    return "\n".join(lines).strip()
