from ..client import get_config, sentry_get


def get_release_deploys(version: str) -> str:
    """
    List all deployments for a specific release version.

    Args:
        version: Full release version (e.g. "com.pajk.idpersonaldoc@5.57.2-c52b693+50105")
    """
    cfg = get_config()
    import urllib.parse
    encoded = urllib.parse.quote(version, safe="")
    path = f"/api/0/organizations/{cfg['org']}/releases/{encoded}/deploys/"
    deploys = sentry_get(path, cfg["token"], cfg["base_url"])

    if not deploys:
        return f"No deployments found for release '{version}'."

    lines = [f"Deployments for {version}:"]
    for d in deploys:
        env = d.get("environment", "unknown")
        date = d.get("dateFinished") or d.get("dateStarted", "unknown")
        deploy_id = d.get("id", "")
        lines.append(f"  [{deploy_id}] env={env}  date={date}")

    return "\n".join(lines)
