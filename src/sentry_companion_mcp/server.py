from mcp.server.fastmcp import FastMCP
from .tools.release_health import get_release_health, get_release_adoption, compare_releases
from .tools.issues import get_release_new_issues, get_release_regressed_issues
from .tools.deploys import get_release_deploys

mcp = FastMCP(
    "sentry-companion",
    instructions=(
        "Companion MCP for Sentry. Provides release health metrics (CFU, adoption, "
        "crash-free rates) and other tools not available in the official Sentry MCP."
    ),
)

mcp.tool()(get_release_health)
mcp.tool()(get_release_adoption)
mcp.tool()(compare_releases)
mcp.tool()(get_release_new_issues)
mcp.tool()(get_release_regressed_issues)
mcp.tool()(get_release_deploys)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
