"""Todoist MCP Server entry point."""

from dotenv import load_dotenv
from fastmcp import FastMCP

from todoist_mcp_server.tools import register_todoist_tools

load_dotenv()
mcp = FastMCP("todoist-mcp-server")
register_todoist_tools(mcp)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
