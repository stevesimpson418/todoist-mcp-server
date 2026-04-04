# Todoist MCP Server

[![CI](https://github.com/stevesimpson418/todoist-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/stevesimpson418/todoist-mcp-server/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/stevesimpson418/todoist-mcp-server/graph/badge.svg)](https://codecov.io/gh/stevesimpson418/todoist-mcp-server)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A local MCP server for Todoist task management, designed for use with Claude.

Wraps both the Todoist REST v2 and Sync API v1 to provide comprehensive task management
capabilities through the Model Context Protocol.

## Features

- **Task CRUD** — create, read, update, complete, delete, and move tasks
- **Batch operations** — update multiple tasks in a single API call via the Sync API
- **Project management** — list projects, resolve by name (case-insensitive)
- **Labels** — create, rename, delete, and apply labels to tasks
- **Comments** — read and add comments on tasks (Markdown supported)
- **Completed tasks** — query tasks completed within a date range (weekly review metrics)
- **Graceful degradation** — server starts without Todoist tools if API token is missing

## Setup

### 1. Get your Todoist API token

Go to [Todoist Developer Settings](https://app.todoist.com/app/settings/integrations/developer)
and copy your API token.

### 2. Install

```bash
git clone https://github.com/stevesimpson418/todoist-mcp-server.git
cd todoist-mcp-server

# Install dependencies (creates .venv/ in the project directory)
uv sync
```

> **New to uv?** `uv sync` reads `pyproject.toml`, creates a `.venv/` virtualenv inside the
> project folder, and installs all dependencies into it. You don't need to activate it —
> `uv run <command>` handles that automatically.

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and add your TODOIST_API_TOKEN
```

### 4. Connect to Claude

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

> **Tip:** Run `uv run which python` from the project directory to get the exact path for `command`.

```json
{
  "mcpServers": {
    "todoist": {
      "command": "/absolute/path/to/todoist-mcp-server/.venv/bin/python",
      "args": ["-m", "todoist_mcp_server.server"],
      "env": {
        "TODOIST_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

Or for Claude Code (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "todoist": {
      "command": "/absolute/path/to/todoist-mcp-server/.venv/bin/todoist-mcp",
      "env": {
        "TODOIST_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Updating

To pull the latest version and update dependencies:

```bash
cd /path/to/todoist-mcp-server
git pull
uv sync
```

Restart Claude Desktop or reload Claude Code after updating.

## Available tools

| Tool | Description |
|------|-------------|
| `list_todoist_projects` | List all projects |
| `get_project_tasks` | Get tasks from a project |
| `list_todoist_labels` | List all labels |
| `get_completed_tasks` | Query completed tasks by date range |
| `get_task_comments` | Get comments on a task |
| `create_task` | Create a new task |
| `update_task` | Update task fields |
| `move_task` | Move task to another project |
| `complete_task` | Mark task as complete |
| `delete_task` | Permanently delete a task |
| `batch_update_tasks` | Batch update multiple tasks |
| `add_task_comment` | Add a comment to a task |
| `create_todoist_label` | Create a new label |
| `rename_todoist_label` | Rename a label |
| `delete_todoist_label` | Delete a label |

### Usage Examples

**Weekly review — see what you accomplished:**

```text
1. get_completed_tasks(since="2026-03-28", until="2026-04-04")  → completed this week
2. list_todoist_projects()                                       → see all projects
3. get_project_tasks(project_name="Inbox")                       → triage leftover inbox tasks
```

**Reorganise tasks across projects:**

```text
1. get_project_tasks(project_name="Inbox")                          → find tasks to sort
2. move_task(task_id="123456", project_name="Home Renovation")      → move to the right project
3. batch_update_tasks(tasks=[
       {"id": "234567", "labels": ["waiting-on"]},
       {"id": "345678", "priority": 3}
   ])                                                               → bulk tidy-up
```

**Quick capture with context:**

```text
1. create_task(
       content="Review pull request #42",
       project_name="Work",
       due_string="tomorrow 10am",
       priority=3
   )
2. add_task_comment(task_id="456789", content="See https://github.com/org/repo/pull/42")
```

## Development

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=todoist_mcp_server --cov-report=term-missing

# Lint
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/

# Install git hooks
lefthook install
```

### Local `.env` file

When running the server manually outside Claude Desktop/Code (e.g., for development or
debugging), you can create a `.env` file in the project root so the server picks up
the API token without passing environment variables:

```text
TODOIST_API_TOKEN=your_token_here
```

This is only needed for local development. The Claude Desktop and Claude Code configs
pass this value directly via the `env` block.

## Packaging & Distribution

This server is currently distributed as source via git. To install:

```bash
git clone https://github.com/stevesimpson418/todoist-mcp-server.git
cd todoist-mcp-server
uv sync
```

This is the standard distribution model for local-stdio MCP servers today. The project is
already configured for wheel builds via hatchling, so future distribution options include:

- **PyPI** — publish to PyPI, then install with `uv tool install todoist-mcp-server` or
  `pip install todoist-mcp-server`. Would require adding a publish workflow to CI.
- **uvx** — once on PyPI, `uvx todoist-mcp-server` runs the server without cloning the repo.
  Claude Desktop/Code config would point to the uvx-managed binary instead of a local `.venv`.

## License

MIT
