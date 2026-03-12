from ..client import get_config, sentry_get


def _fetch_health(version_fragment: str, days: int) -> list[dict]:
    cfg = get_config()
    params = (
        f"project={cfg['project']}"
        f"&field=sum(session)"
        f"&field=count_unique(user)"
        f"&field=crash_free_rate(session)"
        f"&field=crash_free_rate(user)"
        f"&groupBy=release"
        f"&statsPeriod={days}d"
    )
    data = sentry_get(
        f"/api/0/organizations/{cfg['org']}/sessions/?{params}",
        cfg["token"],
        cfg["base_url"],
    )
    return [
        g for g in data.get("groups", [])
        if version_fragment in g.get("by", {}).get("release", "")
    ]


def get_release_health(version: str, days: int = 3) -> str:
    """
    Fetch CFU, crash-free sessions, session count, and user count for a release.

    Args:
        version: Release version fragment to match (e.g. "5.57" or "5.57.2")
        days: Number of days to look back (default: 3)
    """
    groups = _fetch_health(version, days)
    if not groups:
        return f"No releases found matching '{version}' in the last {days} days."

    lines = []
    for g in groups:
        release = g["by"]["release"]
        t = g["totals"]
        sessions = int(t.get("sum(session)") or 0)
        users = int(t.get("count_unique(user)") or 0)
        cfs = (t.get("crash_free_rate(session)") or 0.0) * 100
        cfu = (t.get("crash_free_rate(user)") or 0.0) * 100

        lines.append(f"Release: {release}")
        lines.append(f"  Sessions        : {sessions:,}")
        lines.append(f"  Users           : {users:,}")
        lines.append(f"  Crash-free sessions : {cfs:.2f}%")
        lines.append(f"  Crash-free users    : {cfu:.2f}%")
        lines.append("")

    return "\n".join(lines).strip()


def get_release_adoption(version: str, days: int = 3) -> str:
    """
    Fetch session-based and user-based adoption percentage for a release.

    Adoption = sessions/users on this release ÷ total sessions/users across all releases.

    Args:
        version: Release version fragment to match (e.g. "5.57.2")
        days: Number of days to look back (default: 3)
    """
    cfg = get_config()
    params = (
        f"project={cfg['project']}"
        f"&field=sum(session)"
        f"&field=count_unique(user)"
        f"&groupBy=release"
        f"&statsPeriod={days}d"
    )
    data = sentry_get(
        f"/api/0/organizations/{cfg['org']}/sessions/?{params}",
        cfg["token"],
        cfg["base_url"],
    )
    groups = data.get("groups", [])

    total_sessions = sum(int(g["totals"].get("sum(session)") or 0) for g in groups)
    total_users = sum(int(g["totals"].get("count_unique(user)") or 0) for g in groups)

    matched = [g for g in groups if version in g.get("by", {}).get("release", "")]
    if not matched:
        return f"No releases found matching '{version}' in the last {days} days."

    lines = []
    for g in matched:
        release = g["by"]["release"]
        t = g["totals"]
        sessions = int(t.get("sum(session)") or 0)
        users = int(t.get("count_unique(user)") or 0)
        session_adoption = (sessions / total_sessions * 100) if total_sessions else 0.0
        user_adoption = (users / total_users * 100) if total_users else 0.0

        lines.append(f"Release: {release}")
        lines.append(f"  Session adoption : {session_adoption:.2f}%  ({sessions:,} / {total_sessions:,})")
        lines.append(f"  User adoption    : {user_adoption:.2f}%  ({users:,} / {total_users:,})")
        lines.append("")

    return "\n".join(lines).strip()


def compare_releases(version1: str, version2: str, days: int = 7) -> str:
    """
    Compare crash-free users and sessions side-by-side for two releases.

    Args:
        version1: First release version fragment
        version2: Second release version fragment
        days: Number of days to look back (default: 7)
    """
    cfg = get_config()
    params = (
        f"project={cfg['project']}"
        f"&field=sum(session)"
        f"&field=count_unique(user)"
        f"&field=crash_free_rate(session)"
        f"&field=crash_free_rate(user)"
        f"&groupBy=release"
        f"&statsPeriod={days}d"
    )
    data = sentry_get(
        f"/api/0/organizations/{cfg['org']}/sessions/?{params}",
        cfg["token"],
        cfg["base_url"],
    )
    groups = data.get("groups", [])

    def find(fragment: str) -> dict | None:
        for g in groups:
            if fragment in g.get("by", {}).get("release", ""):
                return g
        return None

    g1 = find(version1)
    g2 = find(version2)

    def fmt(g: dict | None, label: str) -> list[str]:
        if not g:
            return [f"{label}: not found in last {days} days"]
        t = g["totals"]
        cfs = (t.get("crash_free_rate(session)") or 0.0) * 100
        cfu = (t.get("crash_free_rate(user)") or 0.0) * 100
        sessions = int(t.get("sum(session)") or 0)
        users = int(t.get("count_unique(user)") or 0)
        return [
            f"{label} — {g['by']['release']}",
            f"  Sessions        : {sessions:,}",
            f"  Users           : {users:,}",
            f"  Crash-free sessions : {cfs:.2f}%",
            f"  Crash-free users    : {cfu:.2f}%",
        ]

    lines = fmt(g1, version1) + [""] + fmt(g2, version2)

    if g1 and g2:
        cfu1 = (g1["totals"].get("crash_free_rate(user)") or 0.0) * 100
        cfu2 = (g2["totals"].get("crash_free_rate(user)") or 0.0) * 100
        delta = cfu2 - cfu1
        sign = "+" if delta >= 0 else ""
        lines += ["", f"CFU delta ({version1} → {version2}): {sign}{delta:.2f}%"]

    return "\n".join(lines)
