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
