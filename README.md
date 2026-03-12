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

## Claude Code Integration

Run once to register the server:

```bash
claude mcp add sentry-companion \
  -e SENTRY_PERSONAL_TOKEN=your_token \
  -e SENTRY_ORG=your-org-slug \
  -e SENTRY_PROJECT=your-project-id \
  -e SENTRY_BASE_URL=https://us.sentry.io \
  -- uvx sentry-companion-mcp
```

Or add manually to your `.mcp.json`:

```json
{
  "mcpServers": {
    "sentry-companion": {
      "type": "stdio",
      "command": "uvx",
      "args": ["sentry-companion-mcp"],
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
