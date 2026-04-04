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
uv sync
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and add your TODOIST_API_TOKEN
```

### 4. Connect to Claude

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

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

Or for Claude Code (`~/.claude.json`):

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

## License

MIT
