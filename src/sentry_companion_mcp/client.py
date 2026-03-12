import os
import urllib.request
import json


def _env(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return val.strip()


def get_config() -> dict:
    return {
        "token": _env("SENTRY_PERSONAL_TOKEN"),
        "org": _env("SENTRY_ORG"),
        "project": _env("SENTRY_PROJECT"),
        "base_url": _env("SENTRY_BASE_URL"),
    }


def sentry_get(path: str, token: str, base_url: str) -> dict | list:
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
