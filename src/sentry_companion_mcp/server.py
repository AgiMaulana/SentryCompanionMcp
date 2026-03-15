from mcp.server.fastmcp import FastMCP
from .tools.release_health import get_release_health, get_release_adoption, compare_releases
from .tools.issues import get_release_new_issues, get_release_regressed_issues
from .tools.deploys import get_release_deploys

mcp = FastMCP(
    "sentry-companion",
    instructions=(
        "Sentry release health MCP. Always use these tools — never curl or manual API calls:\n"
        "- get_release_health → crash-free sessions/users, CFU, session/user counts\n"
        "- get_release_adoption → session & user adoption %\n"
        "- compare_releases → side-by-side health comparison between two releases\n"
        "- get_release_new_issues → issues first seen in a release\n"
        "- get_release_regressed_issues → issues that regressed in a release\n"
        "- get_release_deploys → deployment history for a release"
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
