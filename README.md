# sentry-companion-mcp

Unofficial Sentry MCP that provide unavailable tools on the official MCP.

## Tools

| Tool | Description |
|---|---|
| `get_release_health` | CFU, crash-free sessions, session and user counts for a release |
| `get_release_adoption` | Session-based and user-based adoption % |
| `compare_releases` | Side-by-side CFU comparison between two releases |
| `get_release_new_issues` | Issues first seen in a specific release |
| `get_release_regressed_issues` | Issues that regressed in a specific release |
| `get_release_deploys` | Deployment history for a release |

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

```env
SENTRY_PERSONAL_TOKEN=your_sentry_personal_token
SENTRY_ORG=your-org-slug
SENTRY_PROJECT=your-project-id
SENTRY_BASE_URL=https://us.sentry.io
```

## Claude Code Integration

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "sentry-companion": {
      "command": "python",
      "args": ["-m", "sentry_companion_mcp.server"],
      "env": {
        "SENTRY_PERSONAL_TOKEN": "your_token",
        "SENTRY_ORG": "your-org-slug",
        "SENTRY_PROJECT": "your-project-id",
        "SENTRY_BASE_URL": "https://us.sentry.io"
      }
    }
  }
}
```
