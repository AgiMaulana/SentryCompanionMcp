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


def get_issue_users(
    issue_id: str,
    organization_slug: str = None,
    limit: int = 100,
    deduplicate_by: str = "email",
    fields: list = None,
) -> str:
    """
    List users affected by a Sentry issue across all events (deduplicated).
    Fills the gap left by the official Sentry MCP which only returns hashed user IDs.

    Args:
        issue_id: The Sentry issue ID (e.g. "GOOD-DOCTOR-ANDROID-6XV")
        organization_slug: Organization slug (defaults to configured org)
        limit: Max events to scan (default: 100)
        deduplicate_by: Field to deduplicate on — "email", "id", or "ip_address" (default: "email")
        fields: List of user fields to include. Options: id, email, username, ip_address, name, geo.
                Default: all available fields.
    """
    cfg = get_config()
    org = organization_slug or cfg["org"]
    path = f"/api/0/organizations/{org}/issues/{issue_id}/events/?limit={limit}"

    events = sentry_get(path, cfg["token"], cfg["base_url"])

    if not events:
        return f"No events found for issue '{issue_id}'."

    # Collect all users from events
    all_users = []
    for event in events:
        user = event.get("user", {})
        if user:
            all_users.append(user)

    if not all_users:
        return f"No user information found in {len(events)} events for issue '{issue_id}'."

    # Deduplicate
    seen = set()
    unique_users = []
    for user in all_users:
        key = user.get(deduplicate_by)
        if key is not None:
            if key not in seen:
                seen.add(key)
                unique_users.append(user)
        else:
            # Include users with null dedup key as a single entry
            if None not in seen:
                seen.add(None)
                unique_users.append(user)

    # Filter fields
    all_field_options = ["id", "email", "username", "ip_address", "name", "geo"]
    selected_fields = fields if fields else all_field_options

    filtered_users = []
    for user in unique_users:
        filtered = {}
        for field in selected_fields:
            if field in user and user[field] is not None:
                filtered[field] = user[field]
        if filtered:
            filtered_users.append(filtered)

    if not filtered_users:
        return f"No matching user data found for issue '{issue_id}'."

    result = {
        "issue_id": issue_id,
        "total_events_scanned": len(events),
        "unique_users": len(filtered_users),
        "deduplicated_by": deduplicate_by,
        "users": filtered_users,
    }

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
