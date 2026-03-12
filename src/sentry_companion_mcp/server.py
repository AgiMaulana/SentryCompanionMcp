from mcp.server.fastmcp import FastMCP
from .tools.release_health import get_release_health, get_release_adoption, compare_releases
from .tools.issues import get_release_new_issues, get_release_regressed_issues
from .tools.deploys import get_release_deploys

mcp = FastMCP(
    "sentry-companion",
    instructions=(
        "Companion MCP for Sentry release health.\n\n"
        "ALWAYS use these tools for Sentry release health — never use curl or manual API calls:\n"
        "- get_release_health → CFU, crash-free sessions, session/user counts for a release\n"
        "- get_release_adoption → session-based and user-based adoption %\n"
        "- compare_releases → side-by-side health comparison between two releases\n"
        "- get_release_new_issues → issues first seen in a specific release\n"
        "- get_release_regressed_issues → issues that regressed in a specific release\n"
        "- get_release_deploys → deployment history for a release\n\n"
        "WHEN TO USE:\n"
        "- User asks for release health, CFU, crash-free rates, or adoption\n"
        "- User shares a Sentry release version string\n"
        "- User asks about new or regressed issues in a release\n"
        "- Daily release monitoring workflows\n\n"
        "Do NOT fall back to curl or REST API calls for data these tools already provide."
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
